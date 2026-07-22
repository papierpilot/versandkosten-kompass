# Changelog

## 2026-07-21 - VERSANDKOMPASS_2026_07_21_BUILD_007

- Änderung: Mehrere Absenderprofile mit UI-Auswahl und Workflow-Anbindung eingeführt.
- Grund: Versandursprung muss bei mehreren Standorten/Absendern fachlich nachvollziehbar sein.
- Risiko: Aktuelle Standortdaten sind Demo-Profile; echte Firmendaten müssen später validiert werden.
- Test: Unit-Tests für Absenderprofile und unterschiedliche Distanzbewertung je Absender.

## 2026-07-21 - VERSANDKOMPASS_2026_07_21_BUILD_006

- Änderung: Mehrpaketsendungen mit unterschiedlichen Maßen und Gewichten über `PackageItem` eingeführt.
- Grund: Reale Mehrpaketsendungen bestehen nicht zwingend aus identischen Paketen.
- Risiko: Simulationspreise sind weiterhin Näherungen; echte Provider-APIs müssen später die Paketliste direkt übernehmen.
- Test: Unit-Tests für explizite Paketlisten, Workflow-Auswertung, Syntax, App-Import und HTTP-Check.

## 2026-07-09 - VERSANDKOMPASS_2026_07_09_BUILD_005

- Änderung: Anbieter Jumingo ergänzt und Kostenbox für getätigte ungebuchte Abholungen eingeführt.
- Grund: Anbieterabdeckung erweitern und offene Abholkosten sichtbar machen.
- Risiko: Simulationswerte sind noch keine echten Jumingo-API-Preise; Abholkosten nutzen aktuell Demo-Daten.
- Test: Anbieter-/Preislogik, Abholkosten-Summe, App-Import und HTTP-Check.

## 2026-07-01 - VERSANDKOMPASS_2026_07_01_BUILD_004

- Änderung: Eingabe-, Prüfungs-, Ergebnis-, Buchungs- und Statusbereiche aus `versand_app.py` nach `ui/` verschoben.
- Grund: `versand_app.py` soll nur noch orchestrieren und Panels verbinden.
- Risiko: Streamlit-Session-State und Buchungsbutton müssen nach dem Verschieben unverändert funktionieren.
- Test: Syntaxprüfung, Unittests inklusive Entscheidungsnotiz, App-Import und HTTP-Check.

## 2026-07-01 - VERSANDKOMPASS_2026_07_01_BUILD_003

- Änderung: Globale Styles, Header und Anbieter-Vergleich aus `versand_app.py` nach `ui/` verschoben.
- Grund: Streamlit-App weiter Richtung Orchestrierung reduzieren und UI-Verantwortung sauber trennen.
- Risiko: HTML/CSS-Darstellung kann durch verschobene Renderfunktionen abweichen.
- Test: Syntaxprüfung, Unittest für Provider-Grid-Rendering, App-Import und HTTP-Check.

## 2026-07-01 - VERSANDKOMPASS_2026_07_01_BUILD_002

- Änderung: `ShipmentInput`, `ShipmentEvaluation` und zentralen `evaluate_shipment()`-Workflow ergänzt.
- Grund: Datenfluss für Markt-/Produktreife nachvollziehbar machen und UI von Bewertungslogik entlasten.
- Risiko: UI-Werte müssen korrekt in den Workflow übertragen werden.
- Test: Unittest-Erweiterung für vollständige Evaluation und sichtbare Warnung bei unvollständiger Adresse.

## 2026-07-01 - VERSANDKOMPASS_2026_07_01_BUILD_001

- Änderung: Erste TES-Modularisierung der bestehenden Streamlit-App.
- Grund: `versand_app.py` soll orchestrieren, Fachlogik wandert in klare Module und Services.
- Risiko: Importfehler durch verschobene Funktionen; UI soll fachlich unverändert bleiben.
- Test: AST-Syntaxprüfung und Import-/Kernlogikprüfung ohne Streamlit-Start.

## v0.8.0-tes - BUILD_008

- Zustelltermin-Prüfung für Standard, Express und Kurierbedarf ergänzt.
- Empfehlung berücksichtigt bei angegebenem Termin fristgerechte Anbieter vor reiner Preislogik.
- UI zeigt Zustellfrist, passende Services und Demo-Grenzen sichtbar an.
- Tests für Deadline-Modul und Workflow-Empfehlung ergänzt.

## v0.9.0-tes - BUILD_009

- General Overnight als Kurier-/Overnightanbieter ergänzt.
- Same-Day-Zustellfristen können im Demo-Serviceprofil über General Overnight erfüllt werden.
- Preisaufbau kennzeichnet General Overnight als Demo-Tarif mit offener Preisliste.
- Tests und Dokumentation für General Overnight ergänzt.
