@echo off
setlocal

title DJ Tool Web - Nur ein Browser

cd /d "%~dp0"

if not defined DJ_TOOL_DEVICE_NAME set "DJ_TOOL_DEVICE_NAME=%COMPUTERNAME%-DJTool"

echo ============================================
echo   DJ Tool Web - Nur ein Browser
echo ============================================
echo.
echo [INFO] Geraet: %DJ_TOOL_DEVICE_NAME%
echo.

set "VENV_PY=%CD%\venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
    echo [FEHLER] Kein lokales venv gefunden.
    pause
    exit /b 1
)

echo [INFO] Starte DJ Tool Web...
echo.

echo [1/3] Setup (unsichtbar)...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel >nul 2>&1
"%VENV_PY%" -m pip install -r requirements.txt >nul 2>&1

echo [2/3] Starte Server...
echo.

start "" http://localhost:8501
"%VENV_PY%" -m streamlit run app_STABLE_backup.py --server.headless true --browser.gatherUsageStats false
