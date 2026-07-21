"""
Central shipping evaluation workflow.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_007"
PURPOSE = "Orchestrate input normalization, validation, pricing, and recommendation metrics"
"""

from modules.location_demo import berechne_demo_entfernung_km, normalisiere_plz
from modules.pricing_simulation import (
    berechne_ersparnis,
    ermittle_vertrauensscore,
    simuliere_anbieterpreise_fuer_pakete,
)
from modules.shipment_model import ShipmentEvaluation, ShipmentInput
from modules.shipping_rules import pruefe_plausibilitaet


def evaluate_shipment(shipment: ShipmentInput) -> ShipmentEvaluation:
    """
    Evaluate one shipment from UI input to recommendation-ready result.

    Data contract:
    - Input: ShipmentInput from UI or later ERP/customer data.
    - Output: ShipmentEvaluation with provider results, warning state, and decision metrics.
    - Fehlerfall: Invalid or missing address data is returned as visible warnings, not hidden.
    - Einheit: Gewicht kg, Maße cm, Entfernung km, Preise EUR.
    - Zeitbezug: Current demo state; no live API call in this workflow yet.
    - Quelle: UI input and static demo provider model.
    """
    sender = shipment.sender_profile()
    plz_norm = normalisiere_plz(shipment.plz)
    entfernung_km, entfernung_hinweis = berechne_demo_entfernung_km(plz_norm, shipment.land, sender)

    packages = shipment.package_items()
    ergebnisse = simuliere_anbieterpreise_fuer_pakete(packages, entfernung_km)
    if not ergebnisse:
        raise ValueError("Keine Anbieterergebnisse erzeugt. Provider-Modell prüfen.")

    bestes_ergebnis = next((ergebnis for ergebnis in ergebnisse if ergebnis["moeglich"]), None)
    referenz = ergebnisse[0]

    warnungen = []
    for package in packages:
        package_warnungen = pruefe_plausibilitaet(
            1,
            package.gewicht_kg,
            package.laenge_cm,
            package.breite_cm,
            package.hoehe_cm,
        )
        warnungen.extend(f"Paket {package.position}: {warnung}" for warnung in package_warnungen)
    if len(packages) >= 20:
        warnungen.append("Hohe Paketmenge: Sammelversand kann wirtschaftlicher sein.")
    if not shipment.plz or not shipment.ort:
        warnungen.append(
            "Zieladresse noch unvollständig: Für echte API-Preise sind mindestens Land, PLZ und Ort nötig."
        )

    zulaessig_gesamt = sum(1 for ergebnis in ergebnisse if ergebnis["moeglich"])
    ausgeschlossen_gesamt = len(ergebnisse) - zulaessig_gesamt
    vertrauensscore = ermittle_vertrauensscore(
        zulaessig_gesamt,
        ausgeschlossen_gesamt,
        warnungen,
        bestes_ergebnis,
    )
    ersparnis_betrag, ersparnis_prozent, teuerster_anbieter = berechne_ersparnis(ergebnisse)

    return ShipmentEvaluation(
        input_data=shipment,
        plz_norm=plz_norm,
        entfernung_km=entfernung_km,
        entfernung_hinweis=entfernung_hinweis,
        ergebnisse=ergebnisse,
        bestes_ergebnis=bestes_ergebnis,
        referenz=referenz,
        warnungen=warnungen,
        zulaessig_gesamt=zulaessig_gesamt,
        ausgeschlossen_gesamt=ausgeschlossen_gesamt,
        vertrauensscore=vertrauensscore,
        ersparnis_betrag=ersparnis_betrag,
        ersparnis_prozent=ersparnis_prozent,
        teuerster_anbieter=teuerster_anbieter,
    )
