@echo off
cd /d "%~dp0"

echo DJ Tool wird sauber gestartet...
echo.

python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --browser.serverAddress=localhost

pause