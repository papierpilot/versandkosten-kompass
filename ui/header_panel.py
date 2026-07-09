"""
Header panel for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_003"
PURPOSE = "Render the app header without business logic"
"""

import streamlit as st


def render_header(app_version: str, provider_count: int) -> None:
    """Render the compact product header."""
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
                    <div class="version-badge">{app_version}</div>
                </div>
                <div class="system-subtitle">Automatisierter Anbietervergleich und Versandassistent</div>
            </div>
            <div class="header-note">
                <strong>Standort</strong><br>
                Am Handwerkerhof 3 · 51379 Leverkusen<br>
                {provider_count} aktive Anbieter · Simulation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
