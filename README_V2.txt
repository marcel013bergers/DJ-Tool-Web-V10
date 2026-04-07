DJ Tool V2 Modular Safe

Start:
1. Ordner separat behalten
2. Im Terminal: streamlit run app_modular.py
   oder Start_DJ_Tool_V2_auto_browser.bat doppelklicken

V2:
- app.py bleibt erhalten
- app_STABLE_backup.py bleibt erhalten
- app_modular.py startet jetzt ueber runtime_bootstrap
- wenn lokale DB leer ist, wird Projekt-DB oder Backup genutzt
- wenn Projekt-DB groesser/besser ist als lokale DB, wird sie uebernommen
