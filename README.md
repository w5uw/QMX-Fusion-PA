# QMX-Fusion-PA

QMX Fusion-PA is a single-file browser app for the QRP Labs QMX+ transceiver. It runs in Google Chrome on a Windows PC and talks to the radio over its USB serial (CAT) port and USB audio.

Current version: **v3.23**

## Features

- **CW message bank**: eight message slots saved in the browser. F1 to F8 send them. Nothing is written into the radio's own memories.
- **Panadapter**: a receive-only spectrum and waterfall drawn from the QMX+ I/Q audio stream, with click-to-tune and a Main Tuning knob.
- **PC Receiver**: plays the radio's audio through the PC in USB, LSB, CW and AM, with filters, AGC, Auto Notch and SSB filter presets.
- **Meters**: needle meters for signal, SWR and power. The power meter holds its peak for 2 seconds.
- **Power knob**: sets the radio's Max. PA voltage in 0.1 V steps to lower transmit power. After each change the app brings the audio stream back.
- **TONE button**: sends the radio's built-in 700 + 1900 Hz two-tone test in USB or LSB. It stops by itself after 30 seconds.
- **Auto Tune**: retunes so the strongest signal sits at the target pitch.

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
| `QMX-Fusion-Panadapter-v3.23.html` | The app |
| `qmx_fusion_server.py` | Local web server on port 8737 |
| `Start QMX Fusion.bat` | Starts the server and opens Chrome |
| `default-version.txt` | Picks the version the plain address opens |
| `README.txt` | Setup notes |

## Changes in v3.23

- The on-screen titles now read "Fusion-PA": the header (QMX FUSION-PA PAN), the startup LCD text, the server window and the setup notes.
- Saved settings files are now named `QMX-Fusion-PA-settings-YYYY-MM-DD.json`. Settings files saved by earlier versions still load.

## License

MIT. See [LICENSE](LICENSE).
