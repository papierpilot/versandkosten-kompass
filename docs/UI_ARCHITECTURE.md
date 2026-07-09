# UI-Architektur

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_003"

## Ziel

Die Oberfläche soll vorbereitete Daten anzeigen, aber keine Fachlogik besitzen.

## Aktueller Stand

- `ui/styles.py` enthält globale Streamlit-CSS-Regeln.
- `ui/header_panel.py` rendert den Kopfbereich.
- `ui/provider_panel.py` rendert den Anbieter-Vergleich aus bereits vorbereiteten Ergebnissen.
- `versand_app.py` orchestriert weiterhin die Seite und ruft UI-Bausteine auf.

## Grenze

UI-Dateien dürfen HTML/CSS und Streamlit-Darstellung enthalten. Preisberechnung, Plausibilitätsprüfung, Datenvalidierung und Anbieterentscheidungen bleiben in `modules/` oder `services/`.

## Nächster Ausbau

Die übrigen Eingabe-, Ergebnis-, Buchungs- und Statusbereiche können in weiteren kleinen Builds nach `ui/` verschoben werden.

## Build VERSANDKOMPASS_2026_07_01_BUILD_004

Zusätzlich ausgelagert:

- `ui/input_panel.py`: Eingabe der Sendungsdaten und Anzeige vorbereiteter Prüfwerte.
- `ui/result_panel.py`: Empfehlung, Nutzenanzeige, Entscheidungsnotiz und simulierte Buchung.
- `ui/status_panel.py`: Plausibilitätswarnungen und Systemstatus.

`versand_app.py` verbindet diese Panels und ruft den zentralen Workflow auf. Die fachliche Bewertung bleibt in `modules/shipping_workflow.py`.

