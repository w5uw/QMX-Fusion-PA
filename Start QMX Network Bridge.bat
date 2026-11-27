@echo off
title QMX Network Bridge
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY (where python >nul 2>nul && set PY=python)
if not defined PY (
  echo Python was not found. Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH".
  pause
  goto :eof
)
%PY% -c "import serial, sounddevice, numpy, websockets" >nul 2>nul
if errorlevel 1 (
  echo First run: installing the Python packages the bridge needs...
  %PY% -m pip install --user pyserial sounddevice numpy websockets
)
%PY% qmx_network_bridge.py %*
pause
