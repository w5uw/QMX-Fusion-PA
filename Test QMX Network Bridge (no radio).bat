@echo off
title QMX Network Bridge - TEST MODE (no radio)
echo TEST MODE: a pretend radio, to check the Wi-Fi link before using the real QMX+.
echo.
call "%~dp0Start QMX Network Bridge.bat" --simulate
