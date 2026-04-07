@echo off
cd /d "%~dp0"
start "" cmd /c "for /l %%i in (1,1,10) do (timeout /t 1 >nul & start http://localhost:8501 & exit)"
streamlit run app_modular.py
pause
