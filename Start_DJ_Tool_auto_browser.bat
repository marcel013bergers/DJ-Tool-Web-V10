@echo off
cd /d "%~dp0"

title DJ Tool Starter

echo ===============================
echo        DJ TOOL STARTET
echo ===============================
echo.

echo Tool wird gestartet...
echo.

pip install -r requirements.txt >nul 2>&1

for /f "tokens=14 delims= " %%A in ('ipconfig ^| findstr /C:"IPv4-Adresse" /C:"IPv4 Address"') do (
    set IPADDR=%%A
    goto :ipfound
)

:ipfound
if not defined IPADDR set IPADDR=localhost

echo DJ Tool laeuft jetzt!
echo.
echo Local URL:   http://localhost:8501
echo Network URL: http://%IPADDR%:8501
echo.

start "" http://localhost:8501

streamlit run app.py --server.headless true
pause
