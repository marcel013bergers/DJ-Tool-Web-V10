# Migrations-Checkliste fuer dein DJ Tool

## 1) Code pruefen
- [ ] Gibt es lokale Pfade wie `C:\`, `D:\` oder feste Netzwerkpfade?
- [ ] Gibt es Schreibvorgaenge in Projektordner oder lokale User-Ordner?
- [ ] Sind Imports vollstaendig in `requirements.txt`?
- [ ] Startet die App lokal sauber mit `streamlit run app.py`?

## 2) Datei-Handling pruefen
- [ ] TXT-Import funktioniert mit `st.file_uploader`
- [ ] ZIP-Import funktioniert ohne lokale Spezialpfade
- [ ] Multi-Upload funktioniert stabil
- [ ] Temp-Dateien werden sauber erstellt und wieder entfernt

## 3) State/Session pruefen
- [ ] Nutzt das Tool `st.session_state` fuer UI-Zustaende?
- [ ] Gehen Daten beim Neuladen verloren, die eigentlich bleiben muessen?
- [ ] Muss etwas dauerhaft gespeichert werden?

## 4) Dauerhafte Daten
- [ ] Falls ja: Render Persistent Disk oder externer Speicher geplant
- [ ] Falls nein: Session/temp reicht aus

## 5) Geheimnisse
- [ ] Keine API-Keys oder Passwoerter im Code
- [ ] Secrets als Environment Variables hinterlegt

## 6) Deployment
- [ ] GitHub-Repo angelegt
- [ ] Render Service erstellt
- [ ] Docker Deploy erfolgreich
- [ ] Oeffentlicher Link getestet
- [ ] iPad-Test abgeschlossen

## 7) Nach dem Go-Live
- [ ] Grossen ZIP-Import testen
- [ ] Geburtstag/Sub-Anlass-Erkennung testen
- [ ] Dubletten-Erkennung testen
- [ ] Analyse Hub testen
- [ ] Set Builder testen
- [ ] Live Hilfe testen
