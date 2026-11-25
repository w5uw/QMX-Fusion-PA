QMX FUSION-PA - LOCAL WEB ADDRESS VERSION
=========================================

Why: Chrome hides playback devices (speakers, virtual audio cables) from pages
opened as a file (file://). Opened from http://localhost:8737 it shows them all
and remembers your audio and COM port permissions.

NEEDS: Python 3 (python.org) and Google Chrome.

FIRST TIME
1. Unzip this folder somewhere permanent, e.g. Documents\QMX-Fusion-Local.
2. In your OLD copy (the file:// one): Settings tab > Backup & Move Settings >
   SAVE SETTINGS TO FILE. The file goes to your Downloads folder.
3. Double-click "Start QMX Fusion.bat". A black window opens and Chrome opens
   http://localhost:8737/ . Leave the black window open while you operate.
4. In the new page: Settings tab > Backup & Move Settings > LOAD SETTINGS FROM
   FILE, pick the file from step 2, click OK. The page reloads.
5. Connect the radio (Chrome asks for the COM port and microphone again once).
6. Radio tab > PC Receiver (click the title to open it) > Output: pick your cable (e.g. CABLE Input).

EVERY DAY
Double-click "Start QMX Fusion.bat". Close the black window when finished.
Tip: right-click the .bat > Send to > Desktop (create shortcut).

DEFAULT VERSION
http://localhost:8737/ opens the version named in default-version.txt
(now QMX-Fusion-Panadapter-v3.27.html). To change it, open default-version.txt
in Notepad, type the other file name, save, and restart the .bat.
Delete default-version.txt to always open the newest version instead.

NEW VERSIONS
Drop the new QMX-Fusion-Panadapter-vX.YY.html into this folder; your settings
carry over. While a default is pinned, try the newest one at
http://localhost:8737/latest . Any version stays usable at
http://localhost:8737/QMX-Fusion-Panadapter-vX.YY.html

ONLY ONE SERVER AT A TIME
Only one QMX Fusion-PA server can use http://localhost:8737 at a time. From v3.10,
starting the .bat in a new folder stops the server from the old folder for you.
If the old one is v3.08 or v3.09, close its black window first, then start the
new .bat. The black window shows "Serving folder" so you can see which folder
is in use.

SAFETY
The server only answers this PC (127.0.0.1); other computers cannot reach it.
