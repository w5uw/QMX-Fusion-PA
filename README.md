# QMX-Fusion-PA

QMX Fusion-PA is a single-file browser app for the QRP Labs QMX+ transceiver. The original creator of QMX-Fusion is Paul Harrison/Sparks72 this is an update to his work and effort at creating a really great WebApp for the QMX+ Transceiver. It runs in Google Chrome on a Windows PC and talks to the radio over its USB serial (CAT) port and USB audio.

Current version: **v3.26**

## Features

- **CW message bank**: eight message slots saved in the browser. F1 to F8 send them. Nothing is written into the radio's own memories.
- **Panadapter**: a receive-only spectrum and waterfall drawn from the QMX+ I/Q audio stream, with click-to-tune and a Main Tuning knob.
- **PC Receiver**: plays the radio's audio through the PC in USB, LSB, CW and AM, with filters, AGC, Auto Notch and SSB filter presets.
- **Meters**: needle meters for signal, SWR and power. The power meter holds its peak for 2 seconds.
- **Power knob**: sets the radio's Max. PA voltage in 0.1 V steps to lower transmit power. After each change the app brings the audio stream back.
- **TONE button**: sends the radio's built-in 700 + 1900 Hz two-tone test in USB or LSB. It stops by itself after 30 seconds.
- **Auto Tune**: reads the panadapter spectrum and retunes onto the strongest nearby signal. In CW it puts the carrier on the dial; in USB and LSB it centres the voice 1500 Hz from the dial. Needs the spectrum display running.

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
| `QMX-Fusion-Panadapter-v3.26.html` | The app |
| `qmx_fusion_server.py` | Local web server on port 8737 |
| `Start QMX Fusion.bat` | Starts the server and opens Chrome |
| `default-version.txt` | Picks the version the plain address opens |
| `README.txt` | Setup notes |

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
