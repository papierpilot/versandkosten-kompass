# BUILD_MARKER = "VERSANDKOMPASS_2026_07_22_BUILD_008"
# PURPOSE = "Streamlit orchestration for Versandkosten-Kompass"

import streamlit as st

from config.app_settings import APP_VERSION
from data.demo_data import ANBIETER_MODELLE, SCENARIOS, STAMMDATEN_DEMO
from modules.location_demo import finde_ort_zu_plz
from modules.shipping_workflow import evaluate_shipment
from services.api_config import lade_api_status
from ui.header_panel import render_header
from ui.input_panel import render_input_panel, render_validation_panel
from ui.provider_panel import render_provider_grid
from ui.result_panel import render_result_panel
from ui.status_panel import render_status_panel
from ui.styles import apply_global_styles




st.set_page_config(
    page_title=f"Versandkosten-Kompass {APP_VERSION}",
    page_icon="▣",
    layout="wide"
)


apply_global_styles()





















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



































def main():
    init_state()
    api_status, api_hinweis = lade_api_status()

    render_header(APP_VERSION, len(ANBIETER_MODELLE))

    col_input, col_result, col_compare = st.columns([0.82, 1.03, 1.24], gap="medium")

    with col_input:
        shipment_input = render_input_panel(apply_scenario, uebernehme_stammdaten, sync_ort_from_plz)
        evaluation = evaluate_shipment(shipment_input)
        render_validation_panel(evaluation)

    with col_result:
        produktivmodus = render_result_panel(evaluation)

    with col_compare:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        title = "Anbieter-Vergleich" if not produktivmodus else "Produktivansicht"
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(render_provider_grid(evaluation.ergebnisse, evaluation.bestes_ergebnis, produktivmodus), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        render_status_panel(evaluation, api_status, api_hinweis)


if __name__ == "__main__":
    main()
