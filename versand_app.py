import os
import json
import math
from datetime import datetime
import time

import streamlit as st


APP_VERSION = "v0.4.6"
API_CONFIG_FILE = "api_keys.local.json"


st.set_page_config(
    page_title=f"Versandkosten-Kompass {APP_VERSION}",
    page_icon="▣",
    layout="wide"
)


st.markdown(
    """
    <style>
    :root {
        --bg-deep: #0b0d0f;
        --bg-panel: rgba(22, 25, 27, 0.94);
        --line: rgba(195, 168, 111, 0.30);
        --line-soft: rgba(195, 168, 111, 0.14);
        --text-main: #f1eee6;
        --text-muted: #b7ad9a;
        --accent: #c3a86f;
        --accent-soft: rgba(195, 168, 111, 0.11);
        --ok: #91aa7d;
        --warn: #d6b46f;
        --danger: #c98272;
    }

    .stApp {
        background: linear-gradient(135deg, #090b0d 0%, #111416 52%, #070809 100%);
        color: var(--text-main);
        font-family: "Segoe UI", "Inter", sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; height: 0rem; }
    [data-testid="stToolbar"] { display: none; }
    footer { display: none; }

    .main .block-container {
        padding-top: 0.38rem;
        padding-bottom: 0.28rem;
        max-width: 1600px;
    }

    .compact-header {
        display: grid;
        grid-template-columns: 0.92fr 1.28fr 0.88fr;
        align-items: center;
        gap: 1rem;
        padding: 0.72rem 0.92rem;
        border: 1px solid var(--line);
        border-radius: 15px;
        background:
            linear-gradient(180deg, rgba(195,168,111,0.08), rgba(0,0,0,0.10)),
            rgba(17, 20, 22, 0.96);
        margin-bottom: 0.52rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    }

    .brand-block {
        border-right: 1px solid rgba(195,168,111,0.18);
        padding-right: 1rem;
    }

    .brand-name {
        font-size: 2.08rem;
        line-height: 0.92;
        margin: 0;
        letter-spacing: 0.015em;
        font-weight: 950;
        color: #fff4d8;
    }

    .brand-sub {
        color: var(--text-muted);
        font-size: 0.66rem;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-top: 0.28rem;
    }

    .title-block {
        text-align: left;
    }

    .title-row { display: flex; align-items: baseline; gap: 0.72rem; flex-wrap: wrap; }
    .compact-header h1 {
        font-size: 1.42rem;
        line-height: 1;
        margin: 0;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        font-weight: 900;
    }

    .system-subtitle {
        color: var(--text-muted);
        font-size: 0.76rem;
        letter-spacing: 0.03em;
        margin-top: 0.32rem;
    }

    .version-badge {
        font-size: 0.66rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: var(--accent);
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.17rem 0.48rem;
        background: var(--accent-soft);
        white-space: nowrap;
    }

    .header-note {
        color: var(--text-muted);
        font-size: 0.68rem;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        line-height: 1.45;
        text-align: right;
        white-space: nowrap;
    }

    .header-note strong {
        color: var(--text-main);
        font-weight: 850;
    }

    .panel {
        border: 1px solid var(--line-soft);
        border-radius: 15px;
        padding: 0.64rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.028), rgba(0,0,0,0.12)), var(--bg-panel);
        box-shadow: 0 10px 24px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.025);
        margin-bottom: 0.46rem;
    }

    .section-title {
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.38rem;
    }

    .hint-line {
        color: var(--text-muted);
        font-size: 0.72rem;
        line-height: 1.28;
        margin-top: 0.28rem;
    }

    .winner-card {
        border: 1px solid rgba(195,168,111,0.62);
        border-radius: 15px;
        padding: 0.78rem;
        background: linear-gradient(180deg, rgba(195,168,111,0.15), rgba(0,0,0,0.12)), rgba(18,21,23,0.96);
        min-height: 142px;
    }

    .recommendation {
        color: var(--accent);
        font-size: 0.66rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 850;
        margin-bottom: 0.28rem;
    }

    .winner-name { font-size: 1.28rem; font-weight: 850; margin: 0; }
    .winner-price { font-size: 2.05rem; font-weight: 900; line-height: 1.02; color: #fff4d8; margin-top: 0.18rem; }
    .winner-meta { color: var(--text-muted); font-size: 0.76rem; line-height: 1.32; margin-top: 0.34rem; }

    .mini-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.38rem;
    }

    .mini-box {
        border: 1px solid var(--line-soft);
        border-radius: 12px;
        padding: 0.45rem 0.52rem;
        background: rgba(0,0,0,0.16);
    }
    .mini-label { color: var(--text-muted); font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.09em; }
    .mini-value { color: var(--text-main); font-size: 0.90rem; font-weight: 830; margin-top: 0.10rem; }

    .message-box {
        border: 1px solid rgba(195,168,111,0.18);
        border-radius: 12px;
        padding: 0.50rem 0.56rem;
        background: rgba(0,0,0,0.15);
        color: #d9d0be;
        font-size: 0.74rem;
        line-height: 1.32;
        min-height: 42px;
    }

    .warning-box {
        border-color: rgba(214,180,111,0.26);
        background: rgba(214,180,111,0.075);
        color: #e6d3a8;
    }

    .ok-box {
        border-color: rgba(145,170,125,0.24);
        background: rgba(145,170,125,0.07);
        color: #cdddba;
    }

    .provider-grid {
        display: grid;
        grid-template-columns: 0.34fr 1.55fr 0.78fr 1.16fr;
        width: 100%;
        border: 1px solid var(--line-soft);
        border-radius: 12px;
        overflow: hidden;
        font-size: 0.74rem;
        background: rgba(0,0,0,0.10);
    }
    .provider-head, .provider-cell {
        padding: 0.34rem 0.42rem;
        border-bottom: 1px solid rgba(195,168,111,0.08);
        border-right: 1px solid rgba(195,168,111,0.08);
        min-height: 1.95rem;
    }
    .provider-head {
        color: var(--accent);
        font-size: 0.61rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        font-weight: 850;
        background: rgba(0,0,0,0.18);
    }
    .provider-cell:nth-last-child(-n+4) { border-bottom: none; }
    .provider-cell:nth-child(4n), .provider-head:nth-child(4n) { border-right: none; }
    .provider-sub { color: var(--text-muted); font-size: 0.68rem; margin-top: 0.08rem; }
    .rank { color: var(--accent); font-weight: 850; }
    .price-cell { font-weight: 850; color: #fff4d8; white-space: nowrap; }
    .status-ok { color: var(--ok); font-weight: 750; }
    .status-bad { color: var(--danger); font-weight: 750; }

    .booking-box {
        border: 1px solid rgba(195,168,111,0.38);
        border-radius: 12px;
        padding: 0.54rem 0.62rem;
        background: linear-gradient(180deg, rgba(195,168,111,0.11), rgba(0,0,0,0.15));
        font-size: 0.74rem;
        line-height: 1.36;
        color: #eee4d1;
    }

    .stNumberInput label, .stRadio label, .stCheckbox label, .stTextInput label, .stSelectbox label { font-size: 0.74rem !important; color: var(--text-muted) !important; }
    .stNumberInput input, .stTextInput input {
        background-color: rgba(0,0,0,0.22) !important;
        border-radius: 10px !important;
        border-color: rgba(195,168,111,0.24) !important;
        color: #f2eee4 !important;
        min-height: 1.90rem !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] { min-height: 1.90rem !important; }
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0,0,0,0.22) !important;
        border-radius: 10px !important;
        border-color: rgba(195,168,111,0.24) !important;
        color: #f2eee4 !important;
    }

    .stButton button {
        border-radius: 12px;
        border: 1px solid rgba(195,168,111,0.50);
        background: linear-gradient(135deg, rgba(195,168,111,0.24), rgba(255,255,255,0.045));
        color: #f4eddd;
        font-weight: 850;
        width: 100%;
        min-height: 2.10rem;
        padding-top: 0.22rem;
        padding-bottom: 0.22rem;
    }

    .stButton button:hover {
        border-color: rgba(195,168,111,0.80);
        background: linear-gradient(135deg, rgba(195,168,111,0.34), rgba(255,255,255,0.065));
        color: #ffffff;
    }

    div[role="radiogroup"] { gap: 0.25rem !important; }


    .trust-list {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.22rem;
        margin-top: 0.46rem;
        font-size: 0.74rem;
        color: #e7dcc7;
    }

    .trust-item {
        border: 1px solid rgba(145,170,125,0.18);
        border-radius: 10px;
        padding: 0.28rem 0.42rem;
        background: rgba(145,170,125,0.055);
    }

    .trust-percent {
        font-size: 2.35rem;
        line-height: 1;
        font-weight: 950;
        color: #fff4d8;
        letter-spacing: -0.04em;
    }

    .provider-reason {
        color: var(--text-muted);
        font-size: 0.66rem;
        line-height: 1.22;
        margin-top: 0.12rem;
    }

    .human-note {
        border: 1px solid rgba(195,168,111,0.34);
        border-radius: 12px;
        padding: 0.46rem 0.54rem;
        background: rgba(195,168,111,0.075);
        color: #eadfc9;
        font-size: 0.74rem;
        line-height: 1.34;
        margin-top: 0.46rem;
    }

    .footer-console {
        color: var(--text-muted);
        font-size: 0.62rem;
        opacity: 0.82;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-top: 0.24rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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


def berechne_demo_entfernung_km(empfaenger_plz, land="Deutschland"):
    """
    Grobe Demo-Entfernung vom festen Versandstandort zur Empfänger-PLZ.
    Das ist bewusst keine echte Straßenroute, sondern eine sichtbare Näherung für die Vorführung.
    In der echten API-Version rechnet der Dienstleister die Zone/Strecke selbst.
    """
    if land != "Deutschland":
        return None, "nur für deutschen Demo-Datensatz"

    plz_norm = normalisiere_plz(empfaenger_plz)
    ziel = PLZ_KOORDINATEN_DEMO.get(plz_norm)
    if not ziel:
        return None, "PLZ nicht im Demo-Distanzdatensatz"

    lat1 = math.radians(VERSANDSTANDORT["lat"])
    lon1 = math.radians(VERSANDSTANDORT["lon"])
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


def init_state():
    defaults = {
        "menge": 1,
        "gewicht": 1.0,
        "laenge": 30.0,
        "breite": 20.0,
        "hoehe": 10.0,
        "empfaenger": "",
        "land": "Deutschland",
        "plz": "",
        "ort": "",
        "booking": None,
        "booking_steps": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_scenario(name):
    values = SCENARIOS[name]
    st.session_state["menge"] = values["menge"]
    st.session_state["gewicht"] = values["gewicht"]
    st.session_state["laenge"] = values["laenge"]
    st.session_state["breite"] = values["breite"]
    st.session_state["hoehe"] = values["hoehe"]
    st.session_state["booking"] = None
    st.session_state["booking_steps"] = []


def uebernehme_stammdaten():
    for key, value in STAMMDATEN_DEMO.items():
        st.session_state[key] = value
    st.session_state["booking"] = None
    st.session_state["booking_steps"] = []


def normalisiere_plz(plz):
    return "".join(ch for ch in str(plz or "") if ch.isdigit())[:5]


def finde_ort_zu_plz(plz, land="Deutschland"):
    if land != "Deutschland":
        return ""
    return PLZ_ORT_DEMO.get(normalisiere_plz(plz), "")


def sync_ort_from_plz():
    """
    Demo-Autovervollständigung: PLZ rein, Ort erscheint nach Bestätigung/Fokuswechsel.
    Streamlit aktualisiert Textfelder nicht bei jedem einzelnen Tastendruck, aber beim Rerun.
    Später ersetzen wir das durch echte Kunden-/ERP-Stammdaten oder einen vollständigen PLZ-Datensatz.
    """
    ort = finde_ort_zu_plz(st.session_state.get("plz", ""), st.session_state.get("land", "Deutschland"))
    if ort:
        st.session_state["ort"] = ort
        st.session_state["booking"] = None


def lade_api_status():
    """
    Vorbereitung für spätere echte API-Anbindungen.
    Echte Schlüssel gehören NICHT in app.py, sondern später in api_keys.local.json
    oder in Streamlit Secrets / Umgebungsvariablen.
    """
    status = {modell["name"]: False for modell in ANBIETER_MODELLE}

    if not os.path.exists(API_CONFIG_FILE):
        return status, "Keine lokale API-Datei gefunden. Simulationsmodus aktiv."

    try:
        with open(API_CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        for name in status:
            status[name] = bool(data.get(name.lower(), {}).get("enabled", False))
        return status, "Lokale API-Datei gefunden. Echte API-Aufrufe sind in dieser Version noch deaktiviert."
    except Exception as exc:
        return status, f"API-Datei vorhanden, aber nicht lesbar: {exc}"


def berechne_volumen_gewicht(laenge_cm, breite_cm, hoehe_cm, divisor=5000):
    return (laenge_cm * breite_cm * hoehe_cm) / divisor


def berechne_gurtmass(laenge_cm, breite_cm, hoehe_cm):
    kanten = sorted([laenge_cm, breite_cm, hoehe_cm], reverse=True)
    return kanten[0] + 2 * kanten[1] + 2 * kanten[2]


def ermittle_formatklasse(laenge_cm, breite_cm, hoehe_cm, abrechnungsgewicht):
    max_kante = max(laenge_cm, breite_cm, hoehe_cm)
    gurtmass = berechne_gurtmass(laenge_cm, breite_cm, hoehe_cm)

    if abrechnungsgewicht > 70 or max_kante > 160 or gurtmass > 400:
        return "Stückgut / Spedition"
    if abrechnungsgewicht > 31.5 or max_kante > 120 or gurtmass > 300:
        return "Sperrgut"
    if abrechnungsgewicht > 20 or max_kante > 100 or gurtmass > 250:
        return "Großpaket"
    if abrechnungsgewicht > 10 or max_kante > 80:
        return "Standardpaket schwer"
    return "Standardpaket"


def pruefe_plausibilitaet(paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm):
    warnungen = []
    volumen_liter = (laenge_cm * breite_cm * hoehe_cm) / 1000

    if paket_menge >= 20:
        warnungen.append("Hohe Paketmenge: Sammelversand kann wirtschaftlicher sein.")
    if gewicht_kg < 0.2 and volumen_liter > 40:
        warnungen.append("Sehr geringes Gewicht bei großem Volumen: Maße prüfen.")
    if gewicht_kg > 70:
        warnungen.append("Gewicht pro Paket liegt oberhalb klassischer Paketdienste.")
    if max(laenge_cm, breite_cm, hoehe_cm) > 160:
        warnungen.append("Eine Kante überschreitet typische Paketdienstgrenzen.")
    if berechne_gurtmass(laenge_cm, breite_cm, hoehe_cm) > 400:
        warnungen.append("Gurtmaß sehr groß: wahrscheinlich Stückgut oder Spedition.")

    return warnungen


def ermittle_ausschlussgruende(modell, abrechnungsgewicht, max_kante, gurtmass, formatklasse):
    gruende = []

    if abrechnungsgewicht > modell["max_kg"]:
        gruende.append(f"über {modell['max_kg']:.1f} kg")
    if max_kante > modell["max_kante"]:
        gruende.append(f"Kante über {modell['max_kante']:.0f} cm")
    if gurtmass > modell["max_gurtmass"]:
        gruende.append(f"Gurtmaß über {modell['max_gurtmass']:.0f} cm")
    if formatklasse == "Sperrgut" and not modell["sperrgut_erlaubt"]:
        gruende.append("kein Sperrgut")
    if formatklasse == "Stückgut / Spedition" and not modell["stueckgut_erlaubt"]:
        gruende.append("kein Stückgut")

    return gruende


def berechne_mengenfaktor(paket_menge):
    if paket_menge >= 20:
        return 0.88, "Mengenstaffel ab 20 Paketen"
    if paket_menge >= 10:
        return 0.92, "Mengenstaffel ab 10 Paketen"
    if paket_menge >= 5:
        return 0.96, "Mengenstaffel ab 5 Paketen"
    return 1.00, "keine Mengenstaffel"


def berechne_simulations_dynamik(anbieter_name, paket_menge):
    matrix = {
        "DHL": [(2, 0.86, "Vorteil bei kleinen Standardmengen"), (4, 1.02, "neutrale Kleinmengenstaffel"), (9, 1.08, "bei mittleren Mengen weniger attraktiv"), (19, 1.10, "Sammelmengen nicht optimal"), (999999, 1.14, "Großmengen nicht Paketdienst-Fokus")],
        "Zipmend": [(2, 1.04, "kein Vorteil bei Einzelpaketen"), (4, 0.82, "Vorteil bei kleinen Bündeln"), (9, 0.96, "solide bei Mischmengen"), (19, 1.03, "größere Mengen weniger stark"), (999999, 1.08, "Großmengen nicht Hauptprofil")],
        "UPS": [(2, 1.08, "Einzelpaket nicht günstigstes Profil"), (4, 1.03, "noch kein deutlicher Vorteil"), (9, 0.78, "Vorteil bei mittleren Mengen"), (19, 0.92, "Mengenfenster bleibt interessant"), (999999, 1.00, "Großmengen neutral")],
        "Cargoboard": [(2, 1.30, "Spedition bei kleinen Mengen unattraktiv"), (4, 1.18, "noch zu geringe Bündelung"), (9, 1.02, "Schwelle zur Bündelung"), (19, 0.55, "Vorteil bei Sammelversand"), (999999, 0.34, "starker Vorteil bei Großmengen")],
    }
    for grenze, faktor, hinweis in matrix.get(anbieter_name, [(999999, 1.00, "neutral")]):
        if paket_menge <= grenze:
            return faktor, hinweis
    return 1.00, "neutral"


def euro(value):
    return f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def berechne_ersparnis(ergebnisse):
    moegliche = [e for e in ergebnisse if e.get("moeglich")]
    if len(moegliche) < 2:
        return 0.0, 0.0, None
    guenstig = min(moegliche, key=lambda e: e["preis"])
    teuer = max(moegliche, key=lambda e: e["preis"])
    differenz = max(teuer["preis"] - guenstig["preis"], 0)
    prozent = (differenz / teuer["preis"] * 100) if teuer["preis"] else 0
    return differenz, prozent, teuer


def ermittle_vertrauensscore(zulaessig, ausgeschlossen, warnungen, bestes_ergebnis):
    if not bestes_ergebnis:
        return 0
    score = 98
    if ausgeschlossen > 0:
        score -= min(ausgeschlossen * 3, 9)
    if warnungen:
        score -= min(len(warnungen) * 2, 8)
    if zulaessig <= 1:
        score -= 6
    return max(78, min(score, 99))


def entscheidungsbasis_html(bestes_ergebnis, paket_menge, entfernung_km):
    if not bestes_ergebnis:
        return ""
    punkte = [
        "günstigster zulässiger Anbieter",
        f"{bestes_ergebnis['formatklasse']} erkannt",
        "Gewicht und Volumengewicht geprüft",
        f"Paketanzahl berücksichtigt: {paket_menge}",
        "Anbietergrenzen und Ausschlussregeln geprüft",
    ]
    if entfernung_km is not None:
        punkte.append("Distanz in Demo-Preis berücksichtigt")
    else:
        punkte.append("Zielregion für Demo nicht vollständig bewertbar")
    return "".join(f"<div class='trust-item'>✓ {punkt}</div>" for punkt in punkte)


def begruendung_fuer_anbieter(ergebnis, bestes_ergebnis, guenstigstes_moegliches=None):
    if not ergebnis.get("moeglich"):
        return "Nicht empfohlen: " + ", ".join(ergebnis.get("ausschlussgruende", [])[:2])
    if bestes_ergebnis and ergebnis["anbieter"] == bestes_ergebnis["anbieter"]:
        return "Empfohlen: wirtschaftlichste zulässige Option · keine Ausschlussgründe"
    if bestes_ergebnis:
        diff = ergebnis["preis"] - bestes_ergebnis["preis"]
        if diff > 0:
            return f"Nicht empfohlen: {euro(diff)} teurer · kein Preisvorteil in diesem Szenario"
    return "Zulässig, aber nicht als beste Option bewertet"


def escape_pdf_text(text):
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_demo_label_pdf(booking):
    """
    Erzeugt ein einfaches Demo-PDF ohne externe Bibliotheken.
    Das ist kein echtes Versandlabel, sondern eine sichtbare Simulation des späteren API-Rücklaufs.
    """
    lines = [
        "VERSANDKOSTEN-KOMPASS · DEMO-LABEL",
        "NICHT FÜR DEN ECHTEN VERSAND VERWENDEN",
        "",
        f"Anbieter: {booking['anbieter']}",
        f"Sendungsnummer: {booking['sendungsnummer']}",
        f"Vorgang: {booking['vorgang']}",
        f"Zeit: {booking['zeit']}",
        "",
        f"Empfänger: {booking.get('empfaenger', '-')}",
        f"Versand ab: {booking.get('versandstandort', '-')}",
        f"Ziel: {booking.get('plz', '-')} {booking.get('ort', '-')} · {booking.get('land', '-')}",
        f"Demo-Entfernung: {formatiere_entfernung(booking.get('entfernung_km'))}",
        f"Demo-Distanzfaktor: {formatiere_faktor(booking.get('distanzfaktor', 1.0))}",
        "",
        f"Menge: {booking['menge']} Paket(e)",
        f"Gewicht je Paket: {booking['gewicht']:.2f} kg",
        f"Maße: {booking['masse']}",
        f"Formatklasse: {booking['formatklasse']}",
        f"Simulierter Preis: {euro(booking['preis'])}",
        "",
        "████ ███ █ ████ ██ █ ███ ████",
        "DEMO-CODE · API-ANBINDUNG NOCH NICHT AKTIV",
    ]

    content = ["BT", "/F1 17 Tf", "50 790 Td"]
    first = True
    for line in lines:
        if not first:
            content.append("0 -26 Td")
        first = False
        safe = escape_pdf_text(line)
        content.append(f"({safe}) Tj")
    content.append("ET")
    stream = "\n".join(content)

    objects = []
    objects.append("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objects.append("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objects.append("3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj")
    objects.append("4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj")
    stream_bytes = stream.encode("latin-1", errors="replace")
    objects.append(f"5 0 obj << /Length {len(stream_bytes)} >> stream\n{stream}\nendstream endobj")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj.encode("latin-1", errors="replace"))
        pdf.extend(b"\n")
    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode("ascii"))
    return bytes(pdf)


def simuliere_anbieterpreise(paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm, entfernung_km=None):
    volumen_gewicht = berechne_volumen_gewicht(laenge_cm, breite_cm, hoehe_cm)
    abrechnungsgewicht = max(gewicht_kg, volumen_gewicht)
    formatklasse = ermittle_formatklasse(laenge_cm, breite_cm, hoehe_cm, abrechnungsgewicht)
    max_kante = max(laenge_cm, breite_cm, hoehe_cm)
    gurtmass = berechne_gurtmass(laenge_cm, breite_cm, hoehe_cm)
    mengenfaktor, mengenhinweis = berechne_mengenfaktor(paket_menge)
    distanzfaktor, distanzhinweis = berechne_demo_distanzfaktor(entfernung_km)
    ergebnisse = []

    for modell in ANBIETER_MODELLE:
        ausschlussgruende = ermittle_ausschlussgruende(modell, abrechnungsgewicht, max_kante, gurtmass, formatklasse)
        basis = modell["basis"]
        gewichtskosten = abrechnungsgewicht * modell["kg"]
        handling = modell["handling"]
        zuschlaege = []

        if formatklasse == "Großpaket":
            zuschlaege.append(("Großpaket", 6.50))
        elif formatklasse == "Sperrgut":
            zuschlaege.append(("Sperrgut", 18.00))
        elif formatklasse == "Stückgut / Spedition":
            zuschlaege.append(("Stückgut", 39.00))
        if modell["name"] == "Cargoboard" and formatklasse == "Stückgut / Spedition":
            zuschlaege.append(("Speditionsvorteil", -12.00))
        if modell["name"] == "Zipmend" and paket_menge >= 3:
            zuschlaege.append(("Mengenimpuls", -2.00))
        if modell["name"] == "UPS" and abrechnungsgewicht > 31.5:
            zuschlaege.append(("Schwerpaket", 9.50))

        zuschlag_summe = sum(wert for _, wert in zuschlaege)
        preis_vor_staffel = basis + gewichtskosten + handling + zuschlag_summe
        simulations_faktor, simulations_hinweis = berechne_simulations_dynamik(modell["name"], paket_menge)
        preis_pro_paket = max(preis_vor_staffel * mengenfaktor * simulations_faktor * distanzfaktor, 0)
        gesamtpreis = preis_pro_paket * paket_menge
        moeglich = len(ausschlussgruende) == 0

        preisaufbau = [
            f"Grund {euro(basis)}",
            f"Gewicht {euro(gewichtskosten)}",
            f"Handling {euro(handling)}",
            f"Staffel {mengenfaktor:.2f}",
            f"Distanz {formatiere_faktor(distanzfaktor)}: {distanzhinweis}",
            f"Demo {simulations_faktor:.2f}: {simulations_hinweis}",
        ]
        for name, wert in zuschlaege:
            preisaufbau.append(f"{name} {euro(wert)}")

        ergebnisse.append({
            "anbieter": modell["name"],
            "preis": round(gesamtpreis, 2),
            "preis_pro_paket": round(preis_pro_paket, 2),
            "moeglich": moeglich,
            "profil": modell["profil"],
            "formatklasse": formatklasse,
            "abrechnungsgewicht": abrechnungsgewicht,
            "volumengewicht": volumen_gewicht,
            "gurtmass": gurtmass,
            "ausschlussgruende": ausschlussgruende,
            "preisaufbau": preisaufbau,
            "demo_hinweis": simulations_hinweis,
            "distanzfaktor": distanzfaktor,
            "distanzhinweis": distanzhinweis,
        })

    return sorted(ergebnisse, key=lambda x: (not x["moeglich"], x["preis"]))


def render_provider_grid(ergebnisse, bestes_ergebnis, produktivmodus=False):
    sichtbare = [bestes_ergebnis] if produktivmodus and bestes_ergebnis else ergebnisse
    cells = [
        "<div class='provider-head'>#</div>",
        "<div class='provider-head'>Anbieter</div>",
        "<div class='provider-head'>Preis</div>",
        "<div class='provider-head'>Status</div>",
    ]
    for index, ergebnis in enumerate(sichtbare, start=1):
        if ergebnis["moeglich"]:
            status = "<span class='status-ok'>zulässig</span>"
            preis = euro(ergebnis["preis"])
        else:
            status = f"<span class='status-bad'>{', '.join(ergebnis['ausschlussgruende'][:2])}</span>"
            preis = "—"
        empfehlung = " · Empfehlung" if bestes_ergebnis and ergebnis["anbieter"] == bestes_ergebnis["anbieter"] else ""
        begruendung = begruendung_fuer_anbieter(ergebnis, bestes_ergebnis)
        cells.extend([
            f"<div class='provider-cell'><span class='rank'>{index}</span></div>",
            f"<div class='provider-cell'><strong>{ergebnis['anbieter']}</strong>{empfehlung}<div class='provider-sub'>{ergebnis['formatklasse']}</div></div>",
            f"<div class='provider-cell price-cell'>{preis}</div>",
            f"<div class='provider-cell'>{status}<div class='provider-reason'>{begruendung}</div></div>",
        ])
    return f"<div class='provider-grid'>{''.join(cells)}</div>"


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


def main():
    init_state()
    api_status, api_hinweis = lade_api_status()

    st.markdown(
        f"""
        <div class="compact-header">
            <div class="brand-block">
                <div class="brand-name">TEXTILWAHN</div>
                <div class="brand-sub">Versandprozess · Demonstrator</div>
            </div>
            <div class="title-block">
                <div class="title-row">
                    <h1>Versandkosten-Kompass</h1>
                    <div class="version-badge">{APP_VERSION}</div>
                </div>
                <div class="system-subtitle">Automatisierter Anbietervergleich und Versandassistent</div>
            </div>
            <div class="header-note">
                <strong>Standort</strong><br>
                Am Handwerkerhof 3 · 51379 Leverkusen<br>
                {len(ANBIETER_MODELLE)} aktive Anbieter · Simulation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_input, col_result, col_compare = st.columns([0.82, 1.03, 1.24], gap="medium")

    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Demo-Szenarien</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2, gap="small")
        with s1:
            if st.button("Klein"):
                apply_scenario("Kleines Paket")
            if st.button("Sperrgut"):
                apply_scenario("Sperrgut")
        with s2:
            if st.button("Mehrere"):
                apply_scenario("Mehrere Pakete")
            if st.button("Großmenge"):
                apply_scenario("Großmenge")
        st.markdown('<div class="hint-line">Für die Vorführung: ein Klick, andere Lage, anderer Anbieter.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Empfänger / Stammdaten</div>', unsafe_allow_html=True)
        if st.button("Stammdaten übernehmen"):
            uebernehme_stammdaten()
        empfaenger = st.text_input("Empfänger", key="empfaenger", placeholder="später aus Kundendaten")
        z1, z2 = st.columns([0.62, 1.0], gap="small")
        with z1:
            land = st.selectbox("Land", ["Deutschland", "Österreich", "Niederlande", "Belgien", "Frankreich", "Schweiz"], key="land")
        with z2:
            p1, p2 = st.columns([0.58, 1.0], gap="small")
            with p1:
                plz = st.text_input("PLZ", key="plz", on_change=sync_ort_from_plz, max_chars=5)
            auto_ort = finde_ort_zu_plz(plz, land)
            if auto_ort and st.session_state.get("ort") != auto_ort:
                st.session_state["ort"] = auto_ort
                st.session_state["booking"] = None
            with p2:
                ort = st.text_input("Ort", key="ort")
        plz_norm = normalisiere_plz(plz)
        entfernung_km, entfernung_hinweis = berechne_demo_entfernung_km(plz_norm, land)
        if land == "Deutschland" and plz_norm and auto_ort:
            st.markdown(f'<div class="hint-line">PLZ erkannt: {plz_norm} → {auto_ort}. Später aus Kunden-/ERP-Stammdaten.</div>', unsafe_allow_html=True)
        elif land == "Deutschland" and plz_norm:
            st.markdown('<div class="hint-line">PLZ nicht im Demo-Datensatz. Ort kann manuell eingetragen werden.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint-line">Platzhalter für spätere Übernahme aus Kunden-/ERP-Daten.</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hint-line">Versand ab: <strong>{VERSANDSTANDORT["plz"]} {VERSANDSTANDORT["ort"]}</strong> · Entfernung: <strong>{formatiere_entfernung(entfernung_km)}</strong> · {entfernung_hinweis}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Sendungsdaten</div>', unsafe_allow_html=True)
        a, b = st.columns(2, gap="small")
        with a:
            paket_menge = st.number_input("Menge", min_value=1, step=1, key="menge")
        with b:
            gewicht_kg = st.number_input("Gewicht kg", min_value=0.1, step=0.1, format="%.2f", key="gewicht")
        c, d, e = st.columns(3, gap="small")
        with c:
            laenge_cm = st.number_input("Länge", min_value=1.0, step=1.0, key="laenge")
        with d:
            breite_cm = st.number_input("Breite", min_value=1.0, step=1.0, key="breite")
        with e:
            hoehe_cm = st.number_input("Höhe", min_value=1.0, step=1.0, key="hoehe")
        st.markdown('</div>', unsafe_allow_html=True)

        ergebnisse = simuliere_anbieterpreise(paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm, entfernung_km)
        bestes_ergebnis = next((e for e in ergebnisse if e["moeglich"]), None)
        referenz = ergebnisse[0]
        warnungen = pruefe_plausibilitaet(paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm)
        if not plz or not ort:
            warnungen.append("Zieladresse noch unvollständig: Für echte API-Preise sind mindestens Land, PLZ und Ort nötig.")

        zulaessig_gesamt = sum(1 for e in ergebnisse if e["moeglich"])
        ausgeschlossen_gesamt = len(ergebnisse) - zulaessig_gesamt
        vertrauensscore = ermittle_vertrauensscore(zulaessig_gesamt, ausgeschlossen_gesamt, warnungen, bestes_ergebnis)
        ersparnis_betrag, ersparnis_prozent, teuerster_anbieter = berechne_ersparnis(ergebnisse)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Prüfung</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="mini-grid">
                <div class="mini-box"><div class="mini-label">Volumen kg</div><div class="mini-value">{referenz['volumengewicht']:.2f}</div></div>
                <div class="mini-box"><div class="mini-label">Abrechnung kg</div><div class="mini-value">{referenz['abrechnungsgewicht']:.2f}</div></div>
                <div class="mini-box"><div class="mini-label">Gesamt kg</div><div class="mini-value">{referenz['abrechnungsgewicht'] * paket_menge:.2f}</div></div>
                <div class="mini-box"><div class="mini-label">Gurtmaß</div><div class="mini-value">{referenz['gurtmass']:.0f} cm</div></div>
                <div class="mini-box"><div class="mini-label">Distanz</div><div class="mini-value">{formatiere_entfernung(entfernung_km)}</div></div>
                <div class="mini-box"><div class="mini-label">Distanzfaktor</div><div class="mini-value">{formatiere_faktor(referenz.get('distanzfaktor', 1.0))}</div></div>
            </div>
            <div class="hint-line">Format: <strong>{referenz['formatklasse']}</strong> · Demo-Distanzlogik: <strong>{referenz.get('distanzhinweis', 'nicht bewertet')}</strong></div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Anzeigemodus</div>', unsafe_allow_html=True)
        anzeigemodus = st.radio(
            "Anzeigemodus",
            ["Vertrauensmodus · alle Anbieter", "Produktivmodus · nur Empfehlung"],
            horizontal=False,
            label_visibility="collapsed",
        )
        produktivmodus = anzeigemodus.startswith("Produktivmodus")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Empfehlung</div>', unsafe_allow_html=True)
        if bestes_ergebnis:
            st.markdown(
                f"""
                <div class="winner-card">
                    <div class="recommendation">Empfehlung des Systems</div>
                    <div class="winner-name">{bestes_ergebnis['anbieter']}</div>
                    <div class="winner-price">{euro(bestes_ergebnis['preis'])}</div>
                    <div class="winner-meta">
                        {paket_menge} Paket(e) · {euro(bestes_ergebnis['preis_pro_paket'])} pro Paket<br>
                        {bestes_ergebnis['formatklasse']} · {referenz['abrechnungsgewicht']:.2f} kg Abrechnung / Paket<br>
                        Versand ab {VERSANDSTANDORT['plz']} {VERSANDSTANDORT['ort']} · {formatiere_entfernung(entfernung_km)}<br>
                        Distanzfaktor {formatiere_faktor(bestes_ergebnis.get('distanzfaktor', 1.0))} · {bestes_ergebnis.get('distanzhinweis', 'nicht bewertet')}<br>
                        {bestes_ergebnis['demo_hinweis']}
                    </div>
                    <div class="trust-list">
                        {entscheidungsbasis_html(bestes_ergebnis, paket_menge, entfernung_km)}
                    </div>
                    <div class="human-note">Diese Empfehlung entspricht der Entscheidung, die ein erfahrener Versandmitarbeiter nach manueller Prüfung voraussichtlich ebenfalls treffen würde.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Versand buchen · {bestes_ergebnis['anbieter']}"):
                progress_slot = st.empty()
                schritte = [
                    "Anbieter wird kontaktiert",
                    "Tarif wird ermittelt",
                    "Sendung wird angelegt",
                    "Label wird erzeugt",
                ]
                erledigt = []
                for schritt in schritte:
                    erledigt.append(schritt)
                    progress_html = "<br>".join(f"✓ {item}" for item in erledigt)
                    progress_slot.markdown(f"<div class='booking-box'>{progress_html}</div>", unsafe_allow_html=True)
                    time.sleep(0.42)
                st.session_state["booking_steps"] = erledigt
                st.session_state["booking"] = build_booking(bestes_ergebnis, paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm, empfaenger, land, plz, ort, entfernung_km)
        else:
            st.error("Kein Anbieter kann diese Sendung im aktuellen Simulationsmodell abbilden.")
        st.markdown('</div>', unsafe_allow_html=True)

        if bestes_ergebnis:
            teuerster_name = teuerster_anbieter["anbieter"] if teuerster_anbieter else "—"
            teuerster_preis = euro(teuerster_anbieter["preis"]) if teuerster_anbieter else "—"
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Nutzen & Vertrauen</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="mini-grid">
                    <div class="mini-box"><div class="mini-label">Ersparnis</div><div class="mini-value">{euro(ersparnis_betrag)}</div></div>
                    <div class="mini-box"><div class="mini-label">Gegen {teuerster_name}</div><div class="mini-value">{ersparnis_prozent:.1f} %</div></div>
                    <div class="mini-box"><div class="mini-label">Manuell</div><div class="mini-value">ca. 10 min</div></div>
                    <div class="mini-box"><div class="mini-label">System</div><div class="mini-value">&lt; 3 sek</div></div>
                    <div class="mini-box"><div class="mini-label">Vertrauen</div><div class="mini-value">{vertrauensscore} %</div></div>
                    <div class="mini-box"><div class="mini-label">Geprüft</div><div class="mini-value">{len(ANBIETER_MODELLE)} Anbieter</div></div>
                </div>
                <div class="hint-line">Teuerster zulässiger Anbieter: {teuerster_preis}. Zeitwerte sind Demo-Annahmen und werden später mit realer Ist-Zeit ersetzt.</div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Entscheidungsnotiz</div>', unsafe_allow_html=True)
        zulässig = zulaessig_gesamt
        ausgeschlossen = ausgeschlossen_gesamt
        if bestes_ergebnis:
            note = (
                f"Alle Anbieter geprüft · {zulässig} zulässig · {ausgeschlossen} ausgeschlossen. "
                f"Empfehlung: {bestes_ergebnis['anbieter']}, weil günstigster zulässiger Anbieter bei "
                f"{paket_menge} Paket(en) und {referenz['abrechnungsgewicht']:.2f} kg Abrechnungsgewicht. "
                f"Ziel: {plz or 'ohne PLZ'} {ort or ''}, {land}. "
                f"Demo-Entfernung ab {VERSANDSTANDORT['plz']} {VERSANDSTANDORT['ort']}: {formatiere_entfernung(entfernung_km)}. "
                f"Distanzfaktor: {formatiere_faktor(bestes_ergebnis.get('distanzfaktor', 1.0))} ({bestes_ergebnis.get('distanzhinweis', 'nicht bewertet')})."
            )
            st.markdown(f"<div class='message-box ok-box'>{note}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='message-box warning-box'>Keine zulässige Empfehlung. Maße oder Gewicht müssen geprüft werden.</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if bestes_ergebnis:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Entscheidungssicherheit</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="message-box ok-box">
                    <div class="trust-percent">{vertrauensscore} %</div>
                    <div>Die Empfehlung basiert auf geprüften Sendungsdaten, Anbietergrenzen, Preislogik und Demo-Distanzbewertung.</div>
                    <div class="hint-line">{len(ANBIETER_MODELLE)} Anbieter geprüft · {zulaessig_gesamt} zulässig · {ausgeschlossen_gesamt} ausgeschlossen</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get("booking"):
            booking = st.session_state["booking"]
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Simulierte Buchung</div>', unsafe_allow_html=True)
            steps_html = "<br>".join(f"✓ {item}" for item in st.session_state.get("booking_steps", []))
            if steps_html:
                st.markdown(f"<div class='booking-box'>{steps_html}</div><div style='height:0.38rem'></div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="booking-box">
                    Vorgang: <strong>{booking['vorgang']}</strong><br>
                    Anbieter: {booking['anbieter']} · Preis: {euro(booking['preis'])}<br>
                    Sendungsnummer: <strong>{booking['sendungsnummer']}</strong><br>
                    Label: {booking['label_datei']}<br>
                    Versand ab: {booking.get('versandstandort', '-')}<br>
                    Empfänger: {booking.get('empfaenger', '-')} · {booking.get('plz', '-')} {booking.get('ort', '-')}<br>
                    Entfernung: {formatiere_entfernung(booking.get('entfernung_km'))} · Faktor {formatiere_faktor(booking.get('distanzfaktor', 1.0))}<br>
                    Sendung: {booking['menge']} × {booking['gewicht']:.2f} kg · {booking['masse']}<br>
                    Status: {booking['api_status']}
                </div>
                """,
                unsafe_allow_html=True,
            )
            label_pdf = make_demo_label_pdf(booking)
            st.download_button(
                "Demo-Label herunterladen",
                data=label_pdf,
                file_name=booking["label_datei"],
                mime="application/pdf",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with col_compare:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        title = "Anbieter-Vergleich" if not produktivmodus else "Produktivansicht"
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(render_provider_grid(ergebnisse, bestes_ergebnis, produktivmodus), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Hinweise & Systemstatus</div>', unsafe_allow_html=True)
        if warnungen:
            warn_text = "<br>".join(f"• {warnung}" for warnung in warnungen[:3])
            msg_class = "warning-box"
        else:
            warn_text = "Keine Plausibilitätswarnungen. Sendungsdaten wirken stimmig."
            msg_class = "ok-box"
        aktive = sum(1 for aktiv in api_status.values() if aktiv)
        st.markdown(
            f"""
            <div class="message-box {msg_class}">{warn_text}</div>
            <div style="height:0.38rem"></div>
            <div class="mini-grid">
                <div class="mini-box"><div class="mini-label">Modus</div><div class="mini-value">Simulation</div></div>
                <div class="mini-box"><div class="mini-label">API aktiv</div><div class="mini-value">{aktive}</div></div>
                <div class="mini-box"><div class="mini-label">Version</div><div class="mini-value">{APP_VERSION}</div></div>
                <div class="mini-box"><div class="mini-label">Anbieter</div><div class="mini-value">{len(ANBIETER_MODELLE)}</div></div>
            </div>
            <div class="footer-console">{api_hinweis} · Schlüssel später in {API_CONFIG_FILE}</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
