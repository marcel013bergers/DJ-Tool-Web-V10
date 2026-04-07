DJ Tool V1 modular

Start:
streamlit run app_modular.py

Wichtig:
- app.py bleibt deine bisherige Version
- app_STABLE_backup.py ist die Sicherheitskopie
- app_modular.py ist der neue sichere Startpunkt

Beim Start macht app_modular.py automatisch:
1. vorhandene Live-DB nutzen
2. wenn leer: Projekt-DB uebernehmen
3. wenn besser/verfuegbar: Backup-ZIP einspielen

Du musst nichts extra installieren, wenn dein bisheriges Projekt schon laeuft.
