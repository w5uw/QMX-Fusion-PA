"""QMX Network Bridge (for QMX Fusion-PA v3.37 and later).

Run this on the computer that has the QMX+ plugged into its USB port. It lets
QMX Fusion-PA on another computer on the same Wi-Fi/router control the radio:

  Data port  (default 50001): radio (CAT) commands, both ways.
  Audio port (default 50002): the radio's I/Q receive audio (48 kHz stereo) to the
                             other computer, and PC-mic transmit audio back.

On the other computer: QMX Fusion-PA > Settings > Network Settings, type this
computer's IP address (shown when the bridge starts), then Radio tab > CONNECT NETWORK.

Only computers on your own network can reach it (unless your router forwards the
ports, which you should not do). Close this window to stop.

Options:
  --port COM5          radio COM port (otherwise chosen automatically or asked once)
  --data-port 50001    data port      --audio-port 50002   audio port
  --choose             ask again for the COM port and sound devices
  --list               list COM ports and sound devices, then exit
  --simulate           no radio needed: a pretend radio, for testing the network link
"""
import argparse, asyncio, json, math, os, random, socket, sys, threading, time

VERSION = "1.0 (for QMX Fusion-PA v3.37)"
HERE = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(HERE, "qmx_bridge_settings.json")
RATE = 48000
BLOCK = 1024              # frames per audio packet (about 21 ms)

def say(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)

def need(mod, pipname):
    try:
        return __import__(mod)
    except ImportError:
        print(f"\nMissing Python package '{pipname}'. Install it with:\n    py -3 -m pip install {pipname}\n"
              "(Start QMX Network Bridge.bat does this for you.)")
        input("Press Enter to close.")
        sys.exit(1)

websockets = need("websockets", "websockets")

def load_settings():
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}

def save_settings(s):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as fh:
            json.dump(s, fh, indent=1)
    except Exception as e:
        say(f"Could not save settings: {e}")

def lan_addresses():
    out = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.0.2.1", 9))          # no packet is sent; this just picks the Wi-Fi/LAN address
        out.append(s.getsockname()[0]); s.close()
    except Exception:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip not in out and not ip.startswith("127."):
                out.append(ip)
    except Exception:
        pass
    return out or ["(unknown - run ipconfig)"]

def ask(prompt, options):
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        v = input(f"{prompt} [1-{len(options)}]: ").strip()
        if v.isdigit() and 1 <= int(v) <= len(options):
            return int(v) - 1

# ---------------------------------------------------------------- radio: serial
class SerialRadio:
    def __init__(self, port):
        serial = need("serial", "pyserial")
        self.ser = serial.Serial(port, 115200, timeout=0.05, write_timeout=1)
        self.name = port
        self.on_data = None
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while True:
            try:
                n = self.ser.in_waiting
                b = self.ser.read(n or 1)
                if b and self.on_data:
                    self.on_data(b)
            except Exception as e:
                say(f"Radio COM port error: {e}. Check the USB cable, then restart the bridge.")
                time.sleep(2)

    def write(self, b):
        try:
            self.ser.write(b)
        except Exception as e:
            say(f"Could not send to the radio: {e}")

def choose_serial(settings, forced, again):
    from serial.tools import list_ports
    ports = list(list_ports.comports())
    if forced:
        return forced
    names = [p.device for p in ports]
    if not again and settings.get("com") in names:
        return settings["com"]
    if not ports:
        print("\nNo COM ports found. Plug in the QMX+ USB cable and turn the radio on, then start again.")
        input("Press Enter to close."); sys.exit(1)
    qmx = [p for p in ports if "qmx" in " ".join(str(x) for x in (p.description, p.product, p.manufacturer)).lower()]
    if len(qmx) == 1 and not again:
        pick = qmx[0].device
    elif len(ports) == 1 and not again:
        pick = ports[0].device
    else:
        print("\nWhich COM port is the QMX+?")
        pick = ports[ask("COM port", [f"{p.device}  {p.description}" for p in ports])].device
    settings["com"] = pick
    save_settings(settings)
    return pick

# ---------------------------------------------------------------- radio: sound card
def choose_audio(settings, again):
    sd = need("sounddevice", "sounddevice")
    need("numpy", "numpy")
    devs = sd.query_devices()
    apis = sd.query_hostapis()
    api = lambda d: apis[d["hostapi"]]["name"]
    order = ["Windows WASAPI", "MME", "Windows DirectSound"]
    rank = lambda d: order.index(api(d)) if api(d) in order else 9

    def works(idx, kind):
        try:
            if kind == "in":
                sd.check_input_settings(device=idx, channels=2, samplerate=RATE, dtype="int16")
            else:
                sd.check_output_settings(device=idx, channels=min(2, devs[idx]["max_output_channels"]), samplerate=RATE, dtype="int16")
            return True
        except Exception:
            return False

    def pick(kind):
        key = "audio_in" if kind == "in" else "audio_out"
        chan = "max_input_channels" if kind == "in" else "max_output_channels"
        need_ch = 2 if kind == "in" else 1
        cands = [i for i, d in enumerate(devs) if d[chan] >= need_ch]
        saved = settings.get(key)
        if saved and not again:
            for i in cands:
                if f"{devs[i]['name']} [{api(devs[i])}]" == saved and works(i, kind):
                    return i
        qmx = sorted([i for i in cands if "qmx" in devs[i]["name"].lower()], key=lambda i: rank(devs[i]))
        for i in qmx:
            if not again and works(i, kind):
                settings[key] = f"{devs[i]['name']} [{api(devs[i])}]"
                return i
        if not cands:
            return None
        what = "the QMX+ receive (recording) device" if kind == "in" else "the QMX+ playback (speaker) device"
        print(f"\nWhich sound device is {what}?")
        while True:
            i = cands[ask("Device", [f"{devs[i]['name']}  [{api(devs[i])}]" for i in cands])]
            if works(i, kind):
                settings[key] = f"{devs[i]['name']} [{api(devs[i])}]"
                return i
            print("That device cannot run at 48 kHz 16-bit. Pick another (try the MME one).")

    i_in, i_out = pick("in"), pick("out")
    save_settings(settings)
    return sd, i_in, i_out

class AudioLink:
    """Radio sound card <-> one network client."""
    def __init__(self, loop, sd=None, dev_in=None, dev_out=None, simulate=None):
        self.loop = loop
        self.client = None
        self.queue = asyncio.Queue(maxsize=40)
        self.tx = bytearray()
        self.tx_lock = threading.Lock()
        self.tx_primed = False
        self.sim = simulate
        self.name_in = self.name_out = "simulated"
        if sd is not None:
            import numpy as np
            self.np = np
            devs = sd.query_devices()
            self.name_in = devs[dev_in]["name"] if dev_in is not None else "none"
            self.name_out = devs[dev_out]["name"] if dev_out is not None else "none"
            if dev_in is not None:
                self.inp = sd.InputStream(device=dev_in, channels=2, samplerate=RATE, dtype="int16", blocksize=BLOCK, callback=self._rx)
                self.inp.start()
            if dev_out is not None:
                self.out_ch = min(2, devs[dev_out]["max_output_channels"])
                self.out = sd.OutputStream(device=dev_out, channels=self.out_ch, samplerate=RATE, dtype="int16", blocksize=BLOCK, callback=self._tx)
                self.out.start()

    # sound card thread -> asyncio
    def _rx(self, indata, frames, t, status):
        if self.client is not None:
            self.loop.call_soon_threadsafe(self._put, bytes(indata))

    def _put(self, b):
        if self.queue.full():
            try: self.queue.get_nowait()
            except Exception: pass
        self.queue.put_nowait(b)

    def _tx(self, outdata, frames, t, status):
        need_b = frames * 2
        with self.tx_lock:
            if not self.tx_primed and len(self.tx) >= 4096 * 2:
                self.tx_primed = True
            if self.tx_primed and len(self.tx) >= need_b:
                chunk = bytes(self.tx[:need_b]); del self.tx[:need_b]
            else:
                if self.tx_primed and len(self.tx) < need_b:
                    self.tx_primed = False
                chunk = None
        if chunk is None:
            outdata.fill(0); return
        mono = self.np.frombuffer(chunk, dtype=self.np.int16)
        for c in range(outdata.shape[1]):
            outdata[:, c] = mono

    def tx_audio(self, b):
        with self.tx_lock:
            self.tx.extend(b)
            if len(self.tx) > RATE * 2 // 2:          # more than 0.5 s behind: drop the oldest
                del self.tx[:len(self.tx) - 4096 * 2]

# ---------------------------------------------------------------- pretend radio (--simulate)
class SimRadio:
    name = "simulated radio"
    def __init__(self):
        self.freq = 14074000; self.mode = "2"; self.tx = False; self.on_data = None; self.buf = ""
    def write(self, b):
        self.buf += b.decode("ascii", "ignore")
        while ";" in self.buf:
            cmd, self.buf = self.buf.split(";", 1)
            r = self.answer(cmd.strip())
            if r is not None and self.on_data:
                self.on_data((r + ";").encode())
    def answer(self, c):
        if c in ("FA", "FB"): return f"{c}{self.freq:011d}"
        if c[:2] in ("FA", "FB") and c[2:].isdigit(): self.freq = int(c[2:]); return None
        if c == "IF": return f"IF{self.freq:011d}     +000000000{1 if self.tx else 0}{self.mode}0000"
        if c == "MD": return f"MD{self.mode}"
        if c.startswith("MD") and len(c) == 3: self.mode = c[2]; return None
        if c == "TX": self.tx = True; return None
        if c == "RX": self.tx = False; return None
        if c == "SM": return f"SM{random.randint(20,60):03d}"
        if c == "PC": return "PC005" if self.tx else "PC000"
        if c == "SW": return "SW120" if self.tx else "SW"
        if c == "LC":
            f = self.freq // 10
            return "LC" + f"A{f//100000:2d},{(f//100)%1000:03d},{f%100:02d}".ljust(16) + "SIMULATED QMX+  "
        if c == "ID": return "ID020"
        if c == "AG0": return "AG0050"
        if c == "KS": return "KS020"
        if c == "VN": return "VN1_04_010SIM"
        if c.startswith("MM"): return "?"
        if c == "SS": return "SS2"
        return None

async def sim_audio(link, radio):
    """Pretend I/Q: noise plus a few carriers, including the 60m channel carriers."""
    import numpy as np
    t0 = time.perf_counter(); n = 0; phase = {}
    while True:
        lo = radio.freq - 12000
        targets = [5330500, 5346500, 5371500, 5403500, 5357000, radio.freq + 1500, radio.freq - 7000, radio.freq + 9000]
        k = np.arange(BLOCK)
        i = np.random.normal(0, 0.003, BLOCK); q = np.random.normal(0, 0.003, BLOCK)
        for f in targets:
            off = f - lo
            if -24000 < off < 24000:
                p = phase.get(f, 0.0)
                ang = p + 2 * math.pi * off * k / RATE
                i += 0.05 * np.cos(ang); q += 0.05 * np.sin(ang)
                phase[f] = (p + 2 * math.pi * off * BLOCK / RATE) % (2 * math.pi)
        st = np.empty(BLOCK * 2, dtype=np.int16)
        st[0::2] = np.clip(i * 32767, -32768, 32767); st[1::2] = np.clip(q * 32767, -32768, 32767)
        if link.client is not None:
            link._put(st.tobytes())
        n += BLOCK
        wait = t0 + n / RATE - time.perf_counter()
        if wait > 0: await asyncio.sleep(wait)

# ---------------------------------------------------------------- network
async def main():
    ap = argparse.ArgumentParser(description="QMX Network Bridge")
    ap.add_argument("--port"); ap.add_argument("--data-port", type=int); ap.add_argument("--audio-port", type=int)
    ap.add_argument("--choose", action="store_true"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--simulate", action="store_true")
    a = ap.parse_args()
    settings = load_settings()
    print(f"QMX Network Bridge {VERSION}\n")
    if a.list:
        try:
            from serial.tools import list_ports
            print("COM ports:"); [print("  ", p.device, p.description) for p in list_ports.comports()]
        except ImportError:
            print("pyserial not installed")
        try:
            import sounddevice as sd; print("\nSound devices:"); print(sd.query_devices())
        except ImportError:
            print("sounddevice not installed")
        return
    if settings.get("data_port") == 8740 and settings.get("audio_port") == 8741:   # first v3.37 test defaults
        settings.pop("data_port"); settings.pop("audio_port"); save_settings(settings)
    dport = a.data_port or settings.get("data_port", 50001)
    aport = a.audio_port or settings.get("audio_port", 50002)
    if a.data_port or a.audio_port:
        settings["data_port"], settings["audio_port"] = dport, aport; save_settings(settings)
    loop = asyncio.get_running_loop()

    if a.simulate:
        radio = SimRadio(); link = AudioLink(loop, simulate=True)
        loop.create_task(sim_audio(link, radio))
    else:
        com = choose_serial(settings, a.port, a.choose)
        radio = SerialRadio(com)
        sd, i_in, i_out = choose_audio(settings, a.choose)
        if i_in is None: say("No QMX+ recording device found: spectrum and receive audio will not work.")
        if i_out is None: say("No QMX+ playback device found: PC-mic transmit audio will not work.")
        link = AudioLink(loop, sd, i_in, i_out)

    data_client = {"ws": None}
    def from_radio(b):
        ws = data_client["ws"]
        if ws is not None:
            loop.call_soon_threadsafe(lambda: asyncio.ensure_future(_send(ws, b)))
    async def _send(ws, b):
        try: await ws.send(b)
        except Exception: pass
    radio.on_data = from_radio

    def peer(ws):
        try: return ws.remote_address[0]
        except Exception: return "?"

    async def data_handler(ws, path=None):
        old = data_client["ws"]
        if old is not None:
            say(f"New data connection from {peer(ws)}; closing the earlier one.")
            try: await old.close()
            except Exception: pass
        data_client["ws"] = ws
        say(f"Data connected: {peer(ws)} (radio {radio.name})")
        await ws.send(json.dumps({"type": "hello", "role": "data", "version": VERSION, "detail": f"radio on {radio.name}"}))
        try:
            async for m in ws:
                radio.write(m.encode() if isinstance(m, str) else m)
        except Exception:
            pass
        finally:
            if data_client["ws"] is ws:
                data_client["ws"] = None
            say(f"Data disconnected: {peer(ws)}")

    async def audio_handler(ws, path=None):
        old = link.client
        if old is not None:
            try: await old.close()
            except Exception: pass
        while not link.queue.empty():
            link.queue.get_nowait()
        link.client = ws
        say(f"Audio connected: {peer(ws)} (in: {link.name_in}; out: {link.name_out})")
        await ws.send(json.dumps({"type": "hello", "role": "audio", "rate": RATE, "channels": 2, "format": "s16le",
                                  "detail": f"receive {link.name_in}, transmit {link.name_out}"}))
        async def pump():
            while True:
                b = await link.queue.get()
                await ws.send(b)
        task = asyncio.ensure_future(pump())
        try:
            async for m in ws:
                if isinstance(m, (bytes, bytearray)) and not link.sim:
                    link.tx_audio(m)
        except Exception:
            pass
        finally:
            task.cancel()
            if link.client is ws:
                link.client = None
            say(f"Audio disconnected: {peer(ws)}")

    kw = dict(compression=None, max_size=2**20, ping_interval=10, ping_timeout=20)
    try:
        s1 = await websockets.serve(data_handler, "0.0.0.0", dport, **kw)
        s2 = await websockets.serve(audio_handler, "0.0.0.0", aport, **kw)
    except OSError as e:
        print(f"\nCould not open port {dport} or {aport}: {e}\nIs the bridge already running? Close the other window, or use --data-port/--audio-port.")
        input("Press Enter to close."); return
    ips = ", ".join(lan_addresses())
    print("=" * 66)
    print(f" Radio:        {radio.name}")
    print(f" Receive from: {link.name_in}")
    print(f" Transmit to:  {link.name_out}")
    print(f" This computer's IP address: {ips}")
    print(f" Data port {dport}   Audio port {aport}")
    print(" In QMX Fusion-PA: Settings > Network Settings, type the IP address and")
    print(" ports above, then Radio tab > CONNECT NETWORK.")
    print(" If Windows asks about the firewall, tick Private networks and click Allow.")
    print("=" * 66)
    say("Waiting for QMX Fusion-PA to connect... (close this window to stop)")
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
