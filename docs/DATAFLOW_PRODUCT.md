# Versandkosten-Kompass Datenfluss

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_002"

## Ziel

Der Versandkosten-Kompass soll nicht nur Preise anzeigen, sondern eine nachvollziehbare Versandentscheidung erzeugen.

## Datenvertrag

Input: `ShipmentInput`

- Empfänger
- Land, PLZ, Ort
- Paketmenge
- Gewicht pro Paket in kg
- Länge, Breite, Höhe in cm

Output: `ShipmentEvaluation`

- normalisierte PLZ
- Demo-Entfernung und Hinweis
- vollständige Anbieterergebnisse
- beste zulässige Empfehlung
- Referenzdaten für Volumengewicht, Abrechnungsgewicht und Gurtmaß
- sichtbare Warnungen
- Anzahl zulässiger und ausgeschlossener Anbieter
- Vertrauensscore
- Ersparnis gegen teuersten zulässigen Anbieter

## Ablauf

1. UI sammelt Eingaben.
2. `ShipmentInput` wird gebaut.
3. `evaluate_shipment()` normalisiert die PLZ.
4. Demo-Entfernung wird berechnet.
5. Provider-Simulation berechnet Anbieterpreise und Ausschlüsse.
6. Plausibilitätsprüfung erzeugt sichtbare Warnungen.
7. Workflow erzeugt Empfehlung, Vertrauen und Ersparnis.
8. UI zeigt nur das vorbereitete `ShipmentEvaluation` an.

## Aktuelle Grenze

Dieser Build nutzt weiterhin Simulation. Echte Provider-APIs werden später in `services/provider_clients/` angeschlossen und müssen denselben Datenvertrag bedienen.
