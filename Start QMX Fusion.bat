@echo off
title QMX Fusion-PA local server
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 qmx_fusion_server.py
  goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python qmx_fusion_server.py
  goto :end
)
echo Python was not found. Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH".
pause
:end
