@echo off
cd /d "%~dp0"
start "" cmd /c "timeout /t 3 >nul && start http://localhost:8501"
streamlit run app_modular.py
pause
