"""
Status and warning panels for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_09_BUILD_005"
PURPOSE = "Render system status and workflow warnings from prepared data"
"""

import streamlit as st

from config.app_settings import API_CONFIG_FILE, APP_VERSION
from data.demo_data import ANBIETER_MODELLE
from modules.pickup_costs import summarize_unbooked_pickups
from modules.shipment_model import ShipmentEvaluation
from modules.pricing_simulation import euro


def render_status_panel(evaluation: ShipmentEvaluation, api_status: dict[str, bool], api_hinweis: str) -> None:
    """Render warnings and current simulation/API status."""
    if evaluation.warnungen:
        warn_text = "<br>".join(f"• {warnung}" for warnung in evaluation.warnungen[:3])
        msg_class = "warning-box"
    else:
        warn_text = "Keine Plausibilitätswarnungen. Sendungsdaten wirken stimmig."
        msg_class = "ok-box"

    aktive = sum(1 for aktiv in api_status.values() if aktiv)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Hinweise & Systemstatus</div>', unsafe_allow_html=True)
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

    pickup_summary = summarize_unbooked_pickups()
    pickup_items = "<br>".join(
        f"{item['datum']} · {item['anbieter']} · {item['referenz']} · {euro(float(item.get('kosten') or 0.0))}"
        for item in pickup_summary.items[:4]
    )
    if not pickup_items:
        pickup_items = "Keine ungebuchten Abholungen vorhanden."

    st.markdown(
        f"""
        <div style="height:0.38rem"></div>
        <div class="message-box warning-box">
            <div class="mini-label">Getätigte ungebuchte Abholungen</div>
            <div class="mini-value">{euro(pickup_summary.total_cost)}</div>
            <div class="hint-line">{pickup_summary.count} offene Abholung(en) · Summe noch nicht gebucht</div>
            <div class="footer-console">{pickup_items}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
