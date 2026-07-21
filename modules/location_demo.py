"""
Demo location and distance helpers.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_007"
PURPOSE = "PLZ normalization, demo city lookup, and demo distance factors"
"""

import math

from data.demo_data import PLZ_KOORDINATEN_DEMO, PLZ_ORT_DEMO, VERSANDSTANDORT


def berechne_demo_entfernung_km(empfaenger_plz, land="Deutschland", sender=None):
    """
    Grobe Demo-Entfernung vom gewählten Versandstandort zur Empfänger-PLZ.
    Das ist bewusst keine echte Straßenroute, sondern eine sichtbare Näherung für die Vorführung.
    In der echten API-Version rechnet der Dienstleister die Zone/Strecke selbst.
    """
    sender_land = getattr(sender, "land", VERSANDSTANDORT["land"])
    if land != "Deutschland" or sender_land != "Deutschland":
        return None, "nur für deutschen Demo-Datensatz"

    plz_norm = normalisiere_plz(empfaenger_plz)
    ziel = PLZ_KOORDINATEN_DEMO.get(plz_norm)
    if not ziel:
        return None, "PLZ nicht im Demo-Distanzdatensatz"

    lat1 = math.radians(float(getattr(sender, "lat", VERSANDSTANDORT["lat"])))
    lon1 = math.radians(float(getattr(sender, "lon", VERSANDSTANDORT["lon"])))
    lat2 = math.radians(ziel[0])
    lon2 = math.radians(ziel[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    luftlinie = 6371 * c

    # Grobe Umrechnung von Luftlinie zu praxisnäherer Straßenentfernung.
    # Absichtlich gerundet, weil es ein Demo-Indikator ist.
    demo_strasse = max(1, round(luftlinie * 1.28))
    return demo_strasse, "ca. Straßenentfernung auf PLZ-Basis"


def formatiere_entfernung(entfernung_km):
    if entfernung_km is None:
        return "—"
    return f"ca. {entfernung_km:.0f} km"


def berechne_demo_distanzfaktor(entfernung_km):
    """
    Demo-Faktor für sichtbare Preisreaktion auf Zielentfernung.
    Wird später entfernt, sobald echte Anbieter-APIs Livepreise liefern.
    """
    if entfernung_km is None:
        return 1.00, "keine Distanzbewertung"
    if entfernung_km <= 50:
        return 1.00, "Nahbereich bis 50 km"
    if entfernung_km <= 150:
        return 1.03, "Regionalbereich 51–150 km"
    if entfernung_km <= 300:
        return 1.06, "Fernbereich 151–300 km"
    if entfernung_km <= 500:
        return 1.09, "Langstrecke 301–500 km"
    return 1.12, "Langstrecke über 500 km"


def formatiere_faktor(faktor):
    return f"{faktor:.2f}".replace(".", ",")


def normalisiere_plz(plz):
    return "".join(ch for ch in str(plz or "") if ch.isdigit())[:5]


def finde_ort_zu_plz(plz, land="Deutschland"):
    if land != "Deutschland":
        return ""
    return PLZ_ORT_DEMO.get(normalisiere_plz(plz), "")
