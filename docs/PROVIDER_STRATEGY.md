# Anbieterstrategie

BUILD_MARKER = "VERSANDKOMPASS_2026_07_09_BUILD_005"

## Neuer Anbieter: Jumingo

Jumingo ist als weiterer Simulationsanbieter im zentralen Anbieter-Modell hinterlegt. Die aktuelle Preislogik bleibt Demo-/Simulationslogik und löst keine echten Buchungen aus.

## Datenfluss

1. `data/demo_data.py` enthält das statische Anbieterprofil.
2. `modules/shipping_rules.py` enthält die mengenabhängige Simulationsdynamik.
3. `modules/pricing_simulation.py` bewertet alle Anbieter gemeinsam.
4. `modules/shipping_workflow.py` erzeugt daraus die Empfehlung.
5. `ui/provider_panel.py` zeigt Jumingo automatisch im Vergleich.

## Ungebuchte Abholungen

Die Kostenbox für getätigte, aber ungebuchte Abholungen wird über `modules/pickup_costs.py` berechnet. Aktuell nutzt sie Demo-Daten aus `UNBOOKED_PICKUPS_DEMO`. Später wird diese Quelle durch ERP/TMS-/Abholjournal-Daten ersetzt.


## Absenderprofile

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_007"

Mehrere Absender werden über `modules/sender_profiles.py` bereitgestellt. Provider-APIs sollen später immer den gewählten Absender erhalten, nicht einen hart codierten Standort.
