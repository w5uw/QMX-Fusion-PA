# QMX-Fusion-PA
![QMX Fusion-PA v3.37](Fusion-PA%203.37.png)
QMX Fusion-PA v3.37 on the QMX+: 60m channel 4 (5403.5 kHz) in DIGI, with the CH1 to CH4 channel lines on the spectrum.

QMX Fusion-PA is a single-file browser app for the QRP Labs QMX+ transceiver. The original creator of QMX-Fusion is Paul - DJ0CU/G4ADF this is an update to his work and effort at creating a really great WebApp for the QMX+ Transceiver. It runs in Google Chrome on a Windows PC and talks to the radio over its USB serial (CAT) port and USB audio.

Current version: **v3.37**

## Features

- **CW message bank**: eight message slots saved in the browser. F1 to F8 send them. Nothing is written into the radio's own memories.
- **Panadapter**: a receive-only spectrum and waterfall drawn from the QMX+ I/Q audio stream, with click-to-tune and a Main Tuning knob.
- **PC Receiver**: plays the radio's audio through the PC in USB, LSB, CW and AM, with filters, AGC, Auto Notch and SSB filter presets.
- **Meters**: needle meters for signal, SWR and power. The power meter holds its peak for 2 seconds.
- **Power knob**: sets the radio's Max. PA voltage in 0.1 V steps to lower transmit power. After each change the app brings the audio stream back.
- **PC Mic**: a TX Audio switch picks HAND MIC (the mic plugged into the radio, with a Hand Mic Gain slider) or PC MIC. With PC MIC you talk through a PC microphone or headset. The app sends the mic into the QMX over USB while the radio transmits in USB or LSB, with Mic Gain and a level meter. The Voice Keyer's SEND button transmits recorded messages the same way.
- **TONE button**: sends the radio's built-in 700 + 1900 Hz two-tone test in USB or LSB. It stops by itself after 30 seconds.
- **Clock**: shows local and UTC time side by side, set from internet time services. The local time zone can be chosen, and the QMX clock can be set to local or UTC time.
- **60m channels**: the 60m band button tunes the four US 60m channels only, and the spectrum shows a magenta line for each channel that you can click to tune.
- **Network connection**: run the radio from another computer on your Wi-Fi. The QMX+ plugs into a remote PC that runs the QMX Network Bridge; CONNECT NETWORK links the app to it.
- **Auto Tune**: reads the panadapter spectrum and retunes onto the strongest nearby signal in CW and puts the 700 Hz carrier on the dial.

## Requirements

- QRP Labs QMX+ connected by USB
- Windows PC with Google Chrome (uses Web Serial and Web Audio)
- Python 3 ([python.org](https://www.python.org/)) for the local web server

## Install and run

1. Download this repository (Code > Download ZIP) and unzip it somewhere permanent, for example `Documents\QMX-Fusion-Local`.
2. Double-click `Start QMX Fusion.bat`. A black server window opens, and Chrome opens http://localhost:8737/.
3. Leave the black window open while you operate. Close it when you're finished.

The app runs from a local web address, not straight from the file. That way Chrome lists every playback device and remembers your COM port and audio permissions. The server only accepts connections from your own PC.

`default-version.txt` names the version that opens at http://localhost:8737/. http://localhost:8737/latest opens the newest version in the folder. See `README.txt` for details.

## Files

| File | Purpose |
|---|---|
| `QMX-Fusion-Panadapter-v3.37.html` | The app |
| `qmx_fusion_server.py` | Local web server on port 8737 |
| `Start QMX Fusion.bat` | Starts the server and opens Chrome |
| `default-version.txt` | Picks the version the plain address opens |
| `README.txt` | Setup notes |
| `qmx_network_bridge.py` | Network bridge, runs on the PC the QMX+ is plugged into |
| `Start QMX Network Bridge.bat` | Starts the bridge (installs its Python packages the first time) |
| `Test QMX Network Bridge (no radio).bat` | Starts the bridge with a pretend radio, to test the Wi-Fi link |

## Changes in v3.37
- **60m button fixed.** The app only treated 5351.5 to 5366.5 kHz as 60m, so the button sent the radio to a frequency it did not count as 60m. It now opens on channel 1, 5330.5 kHz.
- **Band buttons set the sideband.** When the mode is USB or LSB, 160m, 80m and 40m select LSB; 30m, 20m, 17m, 15m, 12m, 10m and 6m select USB; 60m selects DIGI. In CW or AM the band buttons leave the mode alone.
- **60m channels.** On 60m the radio is tuned only to the channel frequencies:

  | Channel | Carrier (DIGI, USB) | Centre (CW) |
  |---|---|---|
  | 1 | 5330.5 kHz | 5332.0 kHz |
  | 2 | 5346.5 kHz | 5348.0 kHz |
  | 3 | 5371.5 kHz | 5373.0 kHz |
  | 4 | 5403.5 kHz | 5405.0 kHz |

  - The spectrum and waterfall show a magenta line for each channel. Each line has a CH1 to CH4 label. Click a line or its label to tune to it. Channels outside the 48 kHz view show as arrow labels at the edge, and those can be clicked too.
  - The tuning knob and arrow keys move one channel at a time. Typed frequencies go to the nearest channel.
  - Transmit from the app is refused when the radio is not on a channel. Auto Tune is off on 60m.
  - **On the radio**: Menu > System config > Band limits > None. With ITU Region 2 limits the QMX+ may refuse the carrier frequencies. The app reads this setting and warns if it is not None.
- **Network connection.** Settings tab > Network Settings (below Panel Visibility; click the title to open or close it) holds the bridge computer's IP address, data port (default 50001) and audio port (default 50002). Radio tab > Serial > CONNECT NETWORK connects. See Network setup below.
- Tested on the QMX+.

## Network setup
The QMX+ plugs by USB into a remote Windows PC on the same Wi-Fi router. That PC runs a small program, the bridge, which passes the radio's commands and audio over the network. The PC you operate from only needs Chrome and QMX Fusion-PA.

On the remote PC (the one the QMX+ is plugged into):
1. Install Python 3 from [python.org](https://www.python.org/downloads/) and tick "Add python.exe to PATH".
2. Copy the QMX Fusion Local folder to it and double-click `Start QMX Network Bridge.bat`. The first time, it installs the Python packages it needs.
3. If Windows Firewall asks, tick **Private networks** and click **Allow**.
4. The window shows the PC's IP address (for example 192.168.1.25) and the ports. Leave the window open.

On the PC you operate from:
1. Settings tab > Network Settings (click the title to open it): type the IP address from the bridge window. Leave the ports at 50001 and 50002 unless you changed them.
2. Click TEST CONNECTION. Both the data port and the audio port should show OK.
3. Radio tab > Serial > CONNECT NETWORK. The status reads CONNECTED (NET). The panadapter, PC Receiver and PC Mic use the network audio.

Notes:
- `Test QMX Network Bridge (no radio).bat` runs a pretend radio, so you can check the link before using the real one.
- To pick a different COM port or sound device, run `py -3 qmx_network_bridge.py --choose` on the remote PC. `--list` shows the devices.
- An IP address can change when the router restarts. Your router's settings can reserve one for the remote PC.
- Wi-Fi adds about a tenth of a second of delay, so CW sent from the PC keyboard feels a little behind.
- The bridge has no password. Use it only on your own home network.

## Changes in v3.36
- SWR on SSB voice now matches the two-tone test. The radio's SWR reading runs high at low power, and speech spends most of its time well below its peaks, so voice read higher than the steady two-tone into the same dummy load.
  - The power reading is now requested right before each SWR reading (it used to come about 80 ms later), so each SWR reading is checked against the power at that moment.
  - A reading counts only when that power is at least 0.5 W and at least 60% of the peak power in the last 3 seconds.
- Confirmed on the QMX+.

## Changes in v3.35
- Steadier SWR meter while transmitting. The radio's SWR reading is a single instant value, and with little or no RF going out (CW key-up, pauses in speech, the start of a transmission) it jumps around even into a dummy load.
  - A reading now counts only when the last two power readings are both at least 0.2 W and at least 25% of the recent peak power.
  - The needle and readout show the median of the last 7 counted readings, rounded to 0.1, and hold that value through pauses.
  - Readings above 99:1 are ignored. The meter still shows RX on receive.
- Confirmed on the QMX+.

## Changes in v3.34
- Space bar TX/RX with PC MIC chosen: press once to transmit, again to receive. Esc always returns to receive.
  - Ignored while typing in a text box or list, with HAND MIC chosen, or outside USB and LSB.
  - The space bar no longer scrolls the page or presses a focused button while PC MIC is chosen.
  - A transmission started from the space bar returns to receive by itself after 3 minutes.
  - Confirmed on the QMX+.

## Changes in v3.33
- Hand Mic Gain slider in the PC Mic box (shown with HAND MIC). It reads and writes the radio's SSB > Microphone > Gain menu setting (default 50 dB) with the Menu Manager commands, reads each write back, then reloads the radio's settings. A change made while transmitting is written on return to receive.
- Mic Gain and the level meter, which only apply to the PC mic, are hidden while HAND MIC is chosen.
- After any settings reload (Power knob or Hand Mic Gain), the app sets the SSB source again to match the TX Audio switch.
- On connect, the CAT log shows the radio's saved SSB > Input menu setting.
- Not yet confirmed with a hand mic on the radio.

## Changes in v3.32
- Hand mic fix: after the PC Mic or a Voice Keyer SEND, the radio stayed on USB audio, so a hand mic plugged into the radio keyed the transmitter with no audio.
  - New TX Audio switch in the PC Mic box: HAND MIC or PC MIC. It replaces the "Send PC mic on TX" tick box.
  - HAND MIC sets the radio's SSB input to its mic jack (SS2). PC MIC sets it to USB audio (SS0) and opens the PC microphone.
  - With HAND MIC chosen, the radio goes back to its mic jack after every Voice Keyer SEND, as soon as it returns to receive.
  - On connect with HAND MIC chosen, the app puts the radio back on its mic jack if an earlier session left it on USB audio or the two-tone test.
  - A line under the switch shows the radio's current TX audio source.
  - Not yet confirmed with a hand mic on the radio.

## Changes in v3.31
- Voice Keyer SEND fix: the radio keyed but no audio reached the transmitter.
  - SEND no longer turns the radio's volume to 0 while it transmits.
  - SEND always sets the SSB source to USB audio (SS0) before keying, the same way the PC Mic does.
  - The To Radio audio stream now starts on your first click, so the QMX already has a steady USB audio signal before any TX.
  - Every message is levelled on SEND so its loudest peak reaches the radio at about -3 dB. Quiet recordings get up to +30 dB of gain, and Mic Gain no longer affects messages.
  - The delay between TX and the start of audio is now 200 ms.
  - A status line above the MSG slots shows which device the message went to and how much it was raised. The same details go to the CAT log.

## Changes in v3.30

- Voice Keyer: the SEND button moved under IMPORT, just above the message slots. The top buttons are now RECORD, PLAY, STOP and CLEAR.

## Changes in v3.29

- Voice Keyer (CW & Voice tab): new SEND button sends the recorded message into the QMX+ through To Radio (PC Mic box), in USB or LSB. With Auto TX/RX ticked the radio transmits for the message, then returns to receive.
- PLAY now only plays the message on the PC speakers so you can check the recording. It never transmits and doesn't change the radio's volume.
- STOP stops either one. Shift+F1 to F8 sends a message, the same as SEND.

## Changes in v3.28

- New PC Mic box on the Radio tab (under PC Receiver). Pick a Microphone and the To Radio device (the QMX playback device, picked automatically), then tick "Send PC mic on TX".
- While the radio transmits in USB or LSB, the mic goes into the QMX over USB. The rest of the time the app sends silence. TX, RX and the radio's own PTT all work.
- Ticking the box sets the radio's SSB audio source to USB (SS0). Unticking it puts back the source the radio had before, such as its mic jack.
- Mic Gain slider (0 to 400%) and a level meter. The audio is filtered to about 150 to 2,800 Hz, and peaks are rounded off before they reach the radio.
- The mic pauses while TONE is transmitting, and in CW, AM and DIGI.
- Voice Keyer (CW & Voice tab): PLAY now sends the message into the radio through To Radio, in USB or LSB only. RECORD uses the PC Mic microphone. With Auto TX/RX unticked, PLAY plays the message on the PC speakers so you can listen to it.

## Changes in v3.27

- Fixed the time sync, which showed (SYNC?) because two of its time services had stopped working. It now tries time.now, then timeapi.io, then Cloudflare, with a 5-second limit on each. worldtimeapi.org and worldclockapi.com were removed.
- Fixed a time-zone bug that made the app's internal clock 6 hours fast. QSO log UTC times are now correct; entries saved under v3.26 or earlier may be 6 hours late.
- A failed sync now retries after 1 minute. The CAT log records why it failed, and hovering over the SYNC tag shows details.
- Radio tab: the frequency display box is shorter, and the Connected/Time bar now runs across to the Meter box.
- The bar shows both LOCAL and UTC time. A time-zone picker offers named zones (which follow daylight saving time) and fixed offsets from UTC-12 to UTC+14.
- New QMX picker chooses whether the radio's clock is set to Local (default, as before) or UTC time. Both choices are remembered.

## Changes in v3.26

- Removed the Target CW Pitch setting from the Audio & DSP tab. It no longer affected Auto Tune.
- The PC Receiver "CW pitch" setting (Radio tab) is now the only CW pitch setting. The CW DSP Filter centres on it.

## Changes in v3.25

- Rebuilt Auto Tune. The old version used the audio stream from before the panadapter, so AUTOTUNE NOW turned off I/Q mode and cut the PC audio, and AUTOTUNE ON did nothing.
- Auto Tune now reads the spectrum the panadapter already shows and never touches the audio. The only command it sends is a normal frequency change.
- CW: tunes so the strongest carrier within 800 Hz of the dial sits on the dial.
- USB and LSB: finds the strongest voice signal near the passband and puts its centre 1500 Hz from the dial.
- AUTOTUNE NOW tunes once. AUTOTUNE ON also runs about 1 second after you stop tuning.
- A status line under the buttons shows what Auto Tune did.

## Changes in v3.24

- Removed "PAN" from the titles. The header now reads QMX FUSION-PA, and the startup LCD text reads QMX Fusion-PA at its normal size.

## Changes in v3.23

- The on-screen titles now read "Fusion-PA": the header, the startup LCD text, the server window and the setup notes.
- Saved settings files are now named `QMX-Fusion-PA-settings-YYYY-MM-DD.json`. Settings files saved by earlier versions still load.

## License

MIT. See [LICENSE](LICENSE).
