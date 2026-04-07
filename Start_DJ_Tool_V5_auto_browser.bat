@echo off
setlocal
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 /nobreak >nul && start "" http://localhost:8501"
streamlit run app_modular.py
