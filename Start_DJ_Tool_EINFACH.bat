@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title DJ Tool Web - Einfach Start

echo ==========================================
echo   DJ Tool Web - Einfach Start
echo ==========================================
echo.

set "PY_CMD="
py -3.12 -V >nul 2>&1 && set "PY_CMD=py -3.12"
if not defined PY_CMD (
    py -3.11 -V >nul 2>&1 && set "PY_CMD=py -3.11"
)
if not defined PY_CMD (
    py -V >nul 2>&1 && set "PY_CMD=py"
)
if not defined PY_CMD (
    python -V >nul 2>&1 && set "PY_CMD=python"
)

if not defined PY_CMD (
    echo [FEHLER] Python wurde nicht gefunden.
    echo Bitte Python 3.12 installieren und "Add Python to PATH" aktivieren.
    echo.
    pause
    exit /b 1
)

echo [INFO] Verwende Python: %PY_CMD%

set "APPDATA_DIR=%LOCALAPPDATA%\DJToolWeb"
set "VENV_DIR=%APPDATA_DIR%\venv"
if not exist "%APPDATA_DIR%" mkdir "%APPDATA_DIR%"

echo [1/4] Pruefe lokale Umgebung...
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [INFO] Erstelle lokale Umgebung...
    %PY_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [FEHLER] Virtuelle Umgebung konnte nicht erstellt werden.
        pause
        exit /b 1
    )
)

set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

echo [2/4] Installiere Abhaengigkeiten...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [FEHLER] pip/setuptools/wheel konnten nicht aktualisiert werden.
    pause
    exit /b 1
)

if exist "requirements.txt" (
    "%VENV_PIP%" install -r requirements.txt
    if errorlevel 1 (
        echo [FEHLER] requirements.txt konnte nicht installiert werden.
        echo Tipp: Python 3.12 verwenden.
        pause
        exit /b 1
    )
)

echo [3/4] Setze Umgebungsvariablen...
if "%DJ_TOOL_LOGIN_PASSWORD%"=="" set "DJ_TOOL_LOGIN_PASSWORD=djtool"
set "STREAMLIT_SERVER_HEADLESS=false"
set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"

echo [4/4] Starte DJ Tool Web...
echo.
echo Browser-Adresse:
echo http://localhost:8501
echo.

start "" cmd /c "timeout /t 4 /nobreak >nul & start http://localhost:8501"
"%VENV_PY%" -m streamlit run app_modular.py

echo.
echo DJ Tool wurde beendet.
pause
endlocal
