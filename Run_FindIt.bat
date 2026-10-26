@echo off
title FindIt
cd /d "%~dp0"

echo ==========================================
echo   FindIt - Find it. Return it. Reuse it.
echo ==========================================
echo.

REM ---- 1. Find Python ----
set PY=
py -3 --version >nul 2>&1 && set PY=py -3
if not defined PY (
  python --version >nul 2>&1 && set PY=python
)
if not defined PY (
  echo [!] Python is not installed.
  echo     1. Go to https://www.python.org/downloads/
  echo     2. Install Python 3.12 or 3.13
  echo     3. IMPORTANT: check "Add python.exe to PATH" on the first screen
  echo     4. Then double-click this file again.
  echo.
  start https://www.python.org/downloads/
  pause
  exit /b 1
)

REM ---- 2. One-time setup (kept outside OneDrive so it does not sync) ----
set VENV=%LOCALAPPDATA%\FindIt\venv
if not exist "%VENV%\Scripts\python.exe" (
  echo [1/3] First-time setup. This takes 1-3 minutes...
  %PY% -m venv "%VENV%"
  if errorlevel 1 ( echo [!] Could not create the Python environment. & pause & exit /b 1 )
  "%VENV%\Scripts\python.exe" -m pip install --upgrade pip -q
)
REM Install or update packages (fast when nothing changed)
"%VENV%\Scripts\python.exe" -m pip install -r requirements.txt -q --disable-pip-version-check
if errorlevel 1 ( echo [!] Install failed. Check the internet connection and try again. & pause & exit /b 1 )

REM ---- 3. Demo data (only if there is no database yet) ----
if not exist "findit.db" (
  echo [2/3] Creating demo data...
  "%VENV%\Scripts\python.exe" seed.py
)

REM ---- 4. Start the app ----
echo [3/3] Starting FindIt... your browser will open.
echo.
echo   Keep this window open while you use the app.
echo   To stop the app, close this window.
echo   Demo log in: Jaden  (password 1212)
echo.
start "" http://localhost:8501
"%VENV%\Scripts\python.exe" -m streamlit run app.py --server.headless true --browser.gatherUsageStats false --server.port 8501
pause
