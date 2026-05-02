import streamlit as st


st.set_page_config(
    page_title="Versandkosten-Kompass",
    page_icon="🚀",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 20% 10%, rgba(0, 255, 255, 0.20), transparent 28%),
            radial-gradient(circle at 80% 20%, rgba(140, 80, 255, 0.25), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(255, 0, 120, 0.16), transparent 35%),
            linear-gradient(135deg, #050711 0%, #080b18 45%, #02040a 100%);
        color: #eafcff;
        font-family: "Segoe UI", sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .main .block-container {
        padding-top: 1.5rem;
        max-width: 1350px;
    }

    .ship-frame {
        border: 1px solid rgba(0, 255, 255, 0.35);
        box-shadow:
            0 0 20px rgba(0, 255, 255, 0.25),
            inset 0 0 35px rgba(0, 255, 255, 0.08);
        border-radius: 30px;
        padding: 1.6rem;
        background: rgba(4, 10, 24, 0.72);
        backdrop-filter: blur(12px);
        margin-bottom: 1.4rem;
        position: relative;
    }

    .ship-frame::before {
        content: "";
        position: absolute;
        inset: 10px;
        border-radius: 22px;
        border: 1px dashed rgba(0, 255, 255, 0.18);
        pointer-events: none;
    }

    .hero {
        padding: 2.4rem;
        border-radius: 34px;
        background:
            linear-gradient(135deg, rgba(0,255,255,0.13), rgba(140,80,255,0.16)),
            rgba(255,255,255,0.04);
        border: 1px solid rgba(0,255,255,0.35);
        box-shadow:
            0 0 35px rgba(0,255,255,0.22),
            0 0 90px rgba(140,80,255,0.18);
        margin-bottom: 1.6rem;
    }

    .hero h1 {
        font-size: 3.7rem;
        margin: 0;
        letter-spacing: -0.05em;
        text-shadow: 0 0 22px rgba(0,255,255,0.55);
    }

    .hero p {
        color: #bfefff;
        font-size: 1.08rem;
        max-width: 850px;
        margin-top: 0.8rem;
    }

    .status-row {
        display: flex;
        gap: 0.7rem;
        flex-wrap: wrap;
        margin-top: 1.4rem;
    }

    .status-pill {
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        border: 1px solid rgba(0,255,255,0.35);
        background: rgba(0,255,255,0.08);
        color: #dffcff;
        font-size: 0.85rem;
        box-shadow: 0 0 14px rgba(0,255,255,0.16);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8ffcff;
        margin-bottom: 1rem;
        text-shadow: 0 0 12px rgba(0,255,255,0.55);
    }

    .result-box {
        padding: 1.4rem;
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(0,255,255,0.16), rgba(255,0,120,0.12)),
            rgba(0,0,0,0.22);
        border: 1px solid rgba(0,255,255,0.35);
        box-shadow: inset 0 0 24px rgba(0,255,255,0.10);
        line-height: 1.75;
    }

    .hud-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,255,255,0.75), transparent);
        margin: 1rem 0;
    }

    div[data-testid="stMetric"] {
        background:
            linear-gradient(135deg, rgba(0,255,255,0.10), rgba(255,255,255,0.035));
        border: 1px solid rgba(0,255,255,0.28);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 0 18px rgba(0,255,255,0.12);
    }

    div[data-testid="stMetricLabel"] {
        color: #9eefff;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        text-shadow: 0 0 12px rgba(0,255,255,0.50);
    }

    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"] {
        background-color: rgba(0,0,0,0.28) !important;
        border-radius: 16px !important;
        border-color: rgba(0,255,255,0.28) !important;
        color: #ffffff !important;
    }

    .stRadio {
        padding: 0.4rem 0;
    }

    .stButton button {
        border-radius: 18px;
        border: 1px solid rgba(0,255,255,0.55);
        background: linear-gradient(135deg, rgba(0,255,255,0.25), rgba(140,80,255,0.28));
        color: white;
        font-weight: 800;
        box-shadow: 0 0 18px rgba(0,255,255,0.22);
    }

    .footer-console {
        color: #7fefff;
        font-size: 0.82rem;
        opacity: 0.85;
        letter-spacing: 0.08em;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def berechne_volumen_gewicht(laenge_cm, breite_cm, hoehe_cm, divisor=5000):
    return (laenge_cm * breite_cm * hoehe_cm) / divisor


def main():
    st.markdown(
        """
        <div class="hero">
            <h1>🚀 Versandkosten-Kompass</h1>
            <p>
            Kontrollzentrum für Versandentscheidungen. Keine Tabellenakrobatik,
            kein Bauchgefühl im Nebel — nur Gewicht, Volumen, Tarif und der Kurs
            zum günstigsten Dienstleister.
            </p>
            <div class="status-row">
                <div class="status-pill">SYSTEM: LOCAL</div>
                <div class="status-pill">ENGINE: STREAMLIT</div>
                <div class="status-pill">MODE: TARIF-SCAN</div>
                <div class="status-pill">MISSION: KOSTEN SENKEN</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, middle, right = st.columns([1.05, 1.05, 0.9], gap="large")

    with left:
        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cargo Input</div>', unsafe_allow_html=True)

        paket_menge = st.number_input("Menge der Pakete", min_value=1, value=1, step=1)

        gewicht_kg = st.number_input(
            "Gewicht pro Paket in kg",
            min_value=0.1,
            value=1.0,
            step=0.1,
            format="%.2f"
        )

        st.markdown('<div class="hud-line"></div>', unsafe_allow_html=True)
        st.markdown("#### Paket-Dimensionen")

        col1, col2, col3 = st.columns(3)

        with col1:
            laenge_cm = st.number_input("Länge cm", min_value=1.0, value=30.0, step=1.0)

        with col2:
            breite_cm = st.number_input("Breite cm", min_value=1.0, value=20.0, step=1.0)

        with col3:
            hoehe_cm = st.number_input("Höhe cm", min_value=1.0, value=10.0, step=1.0)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Mission Profile</div>', unsafe_allow_html=True)

        versandart = st.radio(
            "Versandart",
            options=["Inland", "Ausland"],
            horizontal=True
        )

        vergleichsmodus = st.radio(
            "Vergleichsmodus",
            options=[
                "Automatisch den preiswertesten Dienstleister suchen",
                "Händig vergleichen"
            ],
            horizontal=False
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with middle:
        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Carrier Selection</div>', unsafe_allow_html=True)

        versanddienste = st.multiselect(
            "Welche Versanddienste sollen verglichen werden?",
            options=[
                "UPS",
                "DHL",
                "Übercargoboard",
                "Zipmend"
            ],
            default=[
                "UPS",
                "DHL",
                "Übercargoboard",
                "Zipmend"
            ]
        )

        if not versanddienste:
            st.warning("Bitte mindestens einen Versanddienst auswählen.")

        st.markdown('<div class="hud-line"></div>', unsafe_allow_html=True)

        tarifart = st.selectbox(
            "Tarif auswählen",
            options=[
                "Standardtarif",
                "Express",
                "Economy",
                "Paket",
                "Palette",
                "Stückgut",
                "Sondertarif"
            ]
        )

        waehrung = st.selectbox(
            "Währung auswählen",
            options=[
                "EUR - Euro",
                "USD - US-Dollar",
                "GBP - Britisches Pfund",
                "CHF - Schweizer Franken",
                "DKK - Dänische Krone",
                "NOK - Norwegische Krone",
                "SEK - Schwedische Krone",
                "PLN - Polnischer Złoty",
                "CZK - Tschechische Krone",
                "JPY - Japanischer Yen",
                "CNY - Chinesischer Yuan"
            ]
        )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Tarif Scanner</div>', unsafe_allow_html=True)
        st.info("Tarifdaten werden im nächsten Schritt angedockt. Aktuell läuft nur die Eingabe- und Anzeigezentrale.")
        st.button("🔍 Scan vorbereiten")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        volumen_gewicht = berechne_volumen_gewicht(laenge_cm, breite_cm, hoehe_cm)
        abrechnungsgewicht = max(gewicht_kg, volumen_gewicht)

        gesamtgewicht_real = gewicht_kg * paket_menge
        gesamtgewicht_abrechnung = abrechnungsgewicht * paket_menge

        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Flight Data</div>', unsafe_allow_html=True)

        st.metric("Reales Gewicht", f"{gesamtgewicht_real:.2f} kg")
        st.metric("Volumengewicht / Paket", f"{volumen_gewicht:.2f} kg")
        st.metric("Abrechnung / Paket", f"{abrechnungsgewicht:.2f} kg")
        st.metric("Abrechnung gesamt", f"{gesamtgewicht_abrechnung:.2f} kg")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ship-frame">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Command Result</div>', unsafe_allow_html=True)

        if vergleichsmodus == "Automatisch den preiswertesten Dienstleister suchen":
            st.success("Autopilot aktiv: günstigster Dienstleister wird später automatisch markiert.")
        else:
            st.info("Manueller Modus aktiv: Anbieter werden später nebeneinander verglichen.")

        st.markdown(
            f"""
            <div class="result-box">
                <strong>MISSION SUMMARY</strong><br><br>
                Versandart: {versandart}<br>
                Modus: {vergleichsmodus}<br>
                Carrier: {", ".join(versanddienste) if versanddienste else "Keine Auswahl"}<br>
                Tarif: {tarifart}<br>
                Währung: {waehrung}<br><br>
                Pakete: {paket_menge}<br>
                Gewicht / Paket: {gewicht_kg:.2f} kg<br>
                Maße: {laenge_cm:.1f} × {breite_cm:.1f} × {hoehe_cm:.1f} cm<br>
                Abrechnungsgewicht gesamt: {gesamtgewicht_abrechnung:.2f} kg
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="footer-console">NAVIGATION READY · AWAITING TARIF DATA</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()