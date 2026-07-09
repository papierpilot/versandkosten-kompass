"""
Demo data and static simulation models for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_09_BUILD_005"
PURPOSE = "Static demo data used by the simulation layer"
"""

ANBIETER_MODELLE = [
    {
        "name": "DHL",
        "basis": 6.90,
        "kg": 0.74,
        "handling": 1.10,
        "profil": "stark bei Standardpaketen und sauberer Paketlogik",
        "max_kg": 31.5,
        "max_kante": 120,
        "max_gurtmass": 300,
        "sperrgut_erlaubt": False,
        "stueckgut_erlaubt": False,
    },
    {
        "name": "UPS",
        "basis": 8.20,
        "kg": 0.69,
        "handling": 1.40,
        "profil": "stark bei schwereren Paketen und zuverlässiger Laufzeit",
        "max_kg": 70.0,
        "max_kante": 160,
        "max_gurtmass": 400,
        "sperrgut_erlaubt": True,
        "stueckgut_erlaubt": False,
    },
    {
        "name": "Cargoboard",
        "basis": 18.50,
        "kg": 0.42,
        "handling": 3.20,
        "profil": "interessant bei großem Volumen, Stückgut und sperrigen Sendungen",
        "max_kg": 1000.0,
        "max_kante": 240,
        "max_gurtmass": 900,
        "sperrgut_erlaubt": True,
        "stueckgut_erlaubt": True,
    },
    {
        "name": "Zipmend",
        "basis": 7.60,
        "kg": 0.62,
        "handling": 1.25,
        "profil": "aggressiver Simulationspreis bei gemischten Paketgrößen",
        "max_kg": 70.0,
        "max_kante": 160,
        "max_gurtmass": 400,
        "sperrgut_erlaubt": True,
        "stueckgut_erlaubt": False,
    },
    {
        "name": "Jumingo",
        "basis": 7.95,
        "kg": 0.58,
        "handling": 1.35,
        "profil": "stark als Versandplattform für Paketdienste und internationale Optionen",
        "max_kg": 70.0,
        "max_kante": 160,
        "max_gurtmass": 400,
        "sperrgut_erlaubt": True,
        "stueckgut_erlaubt": False,
    },
]


PLZ_ORT_DEMO = {
    # Demo-Datensatz für die Vorführung.
    # Später wird diese Logik durch Kunden-/ERP-Stammdaten oder eine vollständige PLZ-Tabelle ersetzt.
    "44135": "Dortmund",
    "44137": "Dortmund",
    "44139": "Dortmund",
    "50735": "Köln",
    "50667": "Köln",
    "50668": "Köln",
    "50672": "Köln",
    "51371": "Leverkusen",
    "51373": "Leverkusen",
    "51375": "Leverkusen",
    "51377": "Leverkusen",
    "40210": "Düsseldorf",
    "40211": "Düsseldorf",
    "40212": "Düsseldorf",
    "40472": "Düsseldorf",
    "45127": "Essen",
    "45128": "Essen",
    "47051": "Duisburg",
    "46045": "Oberhausen",
    "44787": "Bochum",
    "45657": "Recklinghausen",
    "48143": "Münster",
    "33602": "Bielefeld",
    "20095": "Hamburg",
    "10115": "Berlin",
    "60311": "Frankfurt am Main",
    "70173": "Stuttgart",
    "80331": "München",
    "88361": "Altshausen",
}


VERSANDSTANDORT = {
    "name": "Auftraggeber",
    "strasse": "Am Handwerkerhof 3",
    "plz": "51379",
    "ort": "Leverkusen",
    "land": "Deutschland",
    # Demo-Koordinate für Leverkusen / Opladen.
    # Später wird das nicht mehr gebraucht, weil die Anbieter-API die Strecke/Zone selbst bewertet.
    "lat": 51.0667,
    "lon": 7.0167,
}


PLZ_KOORDINATEN_DEMO = {
    # Grober Demo-Datensatz: PLZ-Zentren / Stadtnäherungen.
    # Zweck: In der Vorführung sichtbar machen, dass das System mit Zielrelationen arbeitet.
    "51379": (51.0667, 7.0167),
    "51371": (51.0450, 6.9670),
    "51373": (51.0330, 6.9900),
    "51375": (51.0300, 7.0500),
    "51377": (51.0600, 7.0850),
    "50735": (50.9730, 6.9600),
    "50667": (50.9380, 6.9570),
    "50668": (50.9500, 6.9600),
    "50672": (50.9400, 6.9400),
    "40210": (51.2200, 6.7900),
    "40211": (51.2300, 6.7900),
    "40212": (51.2250, 6.7800),
    "40472": (51.2800, 6.8100),
    "44135": (51.5140, 7.4660),
    "44137": (51.5120, 7.4560),
    "44139": (51.5000, 7.4700),
    "45127": (51.4560, 7.0120),
    "45128": (51.4450, 7.0120),
    "47051": (51.4330, 6.7620),
    "46045": (51.4720, 6.8500),
    "44787": (51.4820, 7.2160),
    "45657": (51.6150, 7.1970),
    "48143": (51.9620, 7.6250),
    "33602": (52.0240, 8.5330),
    "20095": (53.5500, 10.0000),
    "10115": (52.5320, 13.3840),
    "60311": (50.1120, 8.6820),
    "70173": (48.7780, 9.1800),
    "80331": (48.1370, 11.5750),
    "88361": (47.9330, 9.5330),
}


STAMMDATEN_DEMO = {
    "empfaenger": "Musterkunde GmbH",
    "land": "Deutschland",
    "plz": "44135",
    "ort": "Dortmund",
}


SCENARIOS = {
    "Kleines Paket": {"menge": 1, "gewicht": 1.4, "laenge": 30.0, "breite": 22.0, "hoehe": 12.0},
    "Mehrere Pakete": {"menge": 8, "gewicht": 6.0, "laenge": 45.0, "breite": 32.0, "hoehe": 28.0},
    "Sperrgut": {"menge": 3, "gewicht": 18.0, "laenge": 145.0, "breite": 38.0, "hoehe": 28.0},
    "Großmenge": {"menge": 24, "gewicht": 12.0, "laenge": 60.0, "breite": 40.0, "hoehe": 35.0},
}

UNBOOKED_PICKUPS_DEMO = [
    {
        "datum": "2026-07-08",
        "anbieter": "DHL",
        "referenz": "ABH-20260708-001",
        "beschreibung": "Abholung Ersatzteile ohne Buchungsabschluss",
        "kosten": 12.90,
        "status": "ungebucht",
    },
    {
        "datum": "2026-07-08",
        "anbieter": "UPS",
        "referenz": "ABH-20260708-002",
        "beschreibung": "Express-Abholung Musterpakete, Buchung offen",
        "kosten": 18.40,
        "status": "ungebucht",
    },
    {
        "datum": "2026-07-09",
        "anbieter": "Jumingo",
        "referenz": "ABH-20260709-001",
        "beschreibung": "Plattform-Abholung noch nicht final gebucht",
        "kosten": 9.80,
        "status": "ungebucht",
    },
]

