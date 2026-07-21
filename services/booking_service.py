"""
Booking object creation for the simulation flow.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_006"
PURPOSE = "Create a visible simulated booking result from a selected provider result"
"""

from datetime import datetime

from data.demo_data import VERSANDSTANDORT


def build_booking(bestes_ergebnis, paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm, empfaenger, land, plz, ort, entfernung_km):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    anbieter_code = bestes_ergebnis["anbieter"].upper().replace(" ", "")[:4]
    sendungsnummer = f"SIM-{anbieter_code}-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
    return {
        "vorgang": f"VK-{timestamp}",
        "zeit": now.strftime("%d.%m.%Y %H:%M:%S"),
        "anbieter": bestes_ergebnis["anbieter"],
        "preis": bestes_ergebnis["preis"],
        "menge": paket_menge,
        "gewicht": gewicht_kg,
        "masse": f"{laenge_cm:.0f} × {breite_cm:.0f} × {hoehe_cm:.0f} cm",
        "gesamtgewicht": gewicht_kg,
        "formatklasse": bestes_ergebnis["formatklasse"],
        "sendungsnummer": sendungsnummer,
        "empfaenger": empfaenger or "nicht angegeben",
        "land": land,
        "plz": plz or "nicht angegeben",
        "ort": ort or "nicht angegeben",
        "versandstandort": f"{VERSANDSTANDORT['strasse']} · {VERSANDSTANDORT['plz']} {VERSANDSTANDORT['ort']}",
        "entfernung_km": entfernung_km,
        "distanzfaktor": bestes_ergebnis.get("distanzfaktor", 1.0),
        "distanzhinweis": bestes_ergebnis.get("distanzhinweis", "nicht bewertet"),
        "label_datei": f"demo_label_{sendungsnummer}.pdf",
        "api_status": "Simulation · keine echte Buchung ausgelöst",
    }
