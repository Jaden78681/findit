@echo off
title FindIt - reset demo data
cd /d "%~dp0"
echo This deletes all FindIt data and creates fresh demo data.
choice /m "Continue"
if errorlevel 2 exit /b 0
set VENV=%LOCALAPPDATA%\FindIt\venv
if not exist "%VENV%\Scripts\python.exe" (
  echo Run Run_FindIt.bat first.
  pause
  exit /b 1
)
"%VENV%\Scripts\python.exe" seed.py
echo Done. Now start FindIt again.
pause
