@echo off
cd /d "%~dp0"

echo DJ Tool Web V10 startet...
start "" cmd /c "timeout /t 3 >nul && start http://localhost:8501"
streamlit run app.py
pause
