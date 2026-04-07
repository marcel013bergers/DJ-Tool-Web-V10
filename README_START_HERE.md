# DJ Tool – Web-Startpaket fuer Render

Dieses Paket ist eine Vorlage, damit dein bestehendes Streamlit-Tool stabil online laeuft.

## Empfohlener Weg
- **Hosting:** Render
- **App-Typ:** Docker Web Service
- **Warum:** Dein bestehendes lokales Setup bleibt moeglichst unveraendert, iPad bekommt einen festen Link, und du vermeidest lokale WLAN/FritzBox-Probleme.

## Was du anpassen musst
1. Lege deinen bestehenden Projektcode in dieses Verzeichnis oder uebernehme die Dateien in dein bestehendes Projekt.
2. Benenne deine Startdatei in `app.py` um **oder** passe Dockerfile und `render.yaml` an.
3. Trage alle Python-Pakete in `requirements.txt` ein.
4. Falls dein Tool lokale Dateien dauerhaft speichert, stelle auf einen dieser Wege um:
   - Render Persistent Disk
   - Cloud-Speicher (spaeter, optional)
   - oder nur Session-Dateien, wenn nichts dauerhaft gespeichert werden muss
5. Lege geheime Werte als Render Environment Variables an, nicht im Code.

## Minimaler GitHub-Ablauf
1. GitHub-Account anlegen
2. Neues Repository erstellen
3. Projekt hochladen
4. Bei Render anmelden
5. `New +` -> `Web Service`
6. GitHub-Repo verbinden
7. Docker-Deployment verwenden
8. Nach dem ersten Deploy den Link auf dem iPad testen

## Wichtige Hinweise fuer Streamlit
- Nutze **keine absoluten lokalen Windows-Pfade** wie `C:\...`
- Schreibe keine wichtigen Daten nur lokal auf Platte, wenn du keinen Persistent Disk nutzt
- Rechne damit, dass Deploys/Restarts ein temporaeres Dateisystem leeren koennen
- Stelle sicher, dass Uploads (`st.file_uploader`) und ZIP/TXT-Verarbeitung relativ zum Projekt oder in temp-Ordnern laufen

## Typische Startkommandos lokal zum Testen
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Typische Render-Umgebungsvariablen
- `PORT` wird von Render gesetzt
- Eigene API-Keys oder Passwoerter als Environment Variables anlegen

## Wenn dein Tool Dateien dauerhaft braucht
Dann ist der naechste sinnvolle Schritt:
- erst **Render + Docker**
- dann bei Bedarf **Persistent Disk** oder **S3-kompatiblen Speicher** nachruesten

