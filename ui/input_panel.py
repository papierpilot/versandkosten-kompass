"""
Input and validation panels for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_007"
PURPOSE = "Collect shipment input and render prepared validation data without pricing logic"
"""

from collections.abc import Callable

import streamlit as st

from modules.sender_profiles import list_sender_profiles
from modules.location_demo import (
    berechne_demo_entfernung_km,
    finde_ort_zu_plz,
    formatiere_entfernung,
    formatiere_faktor,
    normalisiere_plz,
)
from modules.shipment_model import PackageItem, ShipmentEvaluation, ShipmentInput


COUNTRIES = ["Deutschland", "Österreich", "Niederlande", "Belgien", "Frankreich", "Schweiz"]


def render_input_panel(
    apply_scenario: Callable[[str], None],
    uebernehme_stammdaten: Callable[[], None],
    sync_ort_from_plz: Callable[[], None],
) -> ShipmentInput:
    """Render input controls and return a typed shipment input object."""
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
    st.markdown(
        '<div class="hint-line">Für die Vorführung: ein Klick, andere Lage, anderer Anbieter.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Absender</div>', unsafe_allow_html=True)
    sender_profiles = list_sender_profiles()
    sender_labels = [sender.display_name for sender in sender_profiles]
    sender_label = st.selectbox("Absender wählen", sender_labels, key="sender_profile")
    sender = sender_profiles[sender_labels.index(sender_label)]
    st.markdown(
        f'<div class="hint-line">Versand ab: <strong>{sender.address_line}</strong></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Empfänger / Stammdaten</div>', unsafe_allow_html=True)
    if st.button("Stammdaten übernehmen"):
        uebernehme_stammdaten()
    empfaenger = st.text_input("Empfänger", key="empfaenger", placeholder="später aus Kundendaten")
    z1, z2 = st.columns([0.62, 1.0], gap="small")
    with z1:
        land = st.selectbox("Land", COUNTRIES, key="land")
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
    entfernung_km, entfernung_hinweis = berechne_demo_entfernung_km(plz_norm, land, sender)
    if land == "Deutschland" and plz_norm and auto_ort:
        st.markdown(
            f'<div class="hint-line">PLZ erkannt: {plz_norm} → {auto_ort}. Später aus Kunden-/ERP-Stammdaten.</div>',
            unsafe_allow_html=True,
        )
    elif land == "Deutschland" and plz_norm:
        st.markdown(
            '<div class="hint-line">PLZ nicht im Demo-Datensatz. Ort kann manuell eingetragen werden.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="hint-line">Platzhalter für spätere Übernahme aus Kunden-/ERP-Daten.</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div class="hint-line">Entfernung ab <strong>{sender.plz} {sender.ort}</strong>: <strong>{formatiere_entfernung(entfernung_km)}</strong> · {entfernung_hinweis}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sendungsdaten</div>', unsafe_allow_html=True)
    unterschiedliche_pakete = st.checkbox("Pakete einzeln erfassen", key="pakete_unterschiedlich")
    packages = ()

    if unterschiedliche_pakete:
        paket_menge = st.number_input("Anzahl Paketzeilen", min_value=1, max_value=8, step=1, key="paket_anzahl_unterschiedlich")
        package_rows = []
        for index in range(1, int(paket_menge) + 1):
            st.markdown(f'<div class="hint-line">Paket {index}</div>', unsafe_allow_html=True)
            p1, p2, p3, p4 = st.columns(4, gap="small")
            with p1:
                gewicht = st.number_input("Gewicht kg", min_value=0.1, step=0.1, format="%.2f", key=f"paket_{index}_gewicht")
            with p2:
                laenge = st.number_input("Länge", min_value=1.0, step=1.0, key=f"paket_{index}_laenge")
            with p3:
                breite = st.number_input("Breite", min_value=1.0, step=1.0, key=f"paket_{index}_breite")
            with p4:
                hoehe = st.number_input("Höhe", min_value=1.0, step=1.0, key=f"paket_{index}_hoehe")
            package_rows.append(
                PackageItem(
                    position=index,
                    gewicht_kg=gewicht,
                    laenge_cm=laenge,
                    breite_cm=breite,
                    hoehe_cm=hoehe,
                )
            )
        packages = tuple(package_rows)
        gewicht_kg = packages[0].gewicht_kg
        laenge_cm = packages[0].laenge_cm
        breite_cm = packages[0].breite_cm
        hoehe_cm = packages[0].hoehe_cm
    else:
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

    return ShipmentInput(
        paket_menge=int(paket_menge),
        gewicht_kg=gewicht_kg,
        laenge_cm=laenge_cm,
        breite_cm=breite_cm,
        hoehe_cm=hoehe_cm,
        empfaenger=empfaenger,
        land=land,
        plz=plz,
        ort=ort,
        packages=packages,
        sender=sender,
    )


def render_validation_panel(evaluation: ShipmentEvaluation) -> None:
    """Render prepared validation values from the workflow evaluation."""
    shipment = evaluation.input_data
    referenz = evaluation.referenz
    package_count = shipment.effective_paket_menge
    total_weight = shipment.total_gewicht_kg
    total_billing_weight = referenz.get("gesamt_abrechnungsgewicht", referenz["abrechnungsgewicht"] * package_count)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Prüfung</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="mini-grid">
            <div class="mini-box"><div class="mini-label">Volumen kg</div><div class="mini-value">{referenz['volumengewicht']:.2f}</div></div>
            <div class="mini-box"><div class="mini-label">Max. Abrechnung kg</div><div class="mini-value">{referenz['abrechnungsgewicht']:.2f}</div></div>
            <div class="mini-box"><div class="mini-label">Gesamt Abrechnung</div><div class="mini-value">{total_billing_weight:.2f} kg</div></div>
            <div class="mini-box"><div class="mini-label">Gurtmaß</div><div class="mini-value">{referenz['gurtmass']:.0f} cm</div></div>
            <div class="mini-box"><div class="mini-label">Pakete</div><div class="mini-value">{package_count}</div></div>
            <div class="mini-box"><div class="mini-label">Realgewicht</div><div class="mini-value">{total_weight:.2f} kg</div></div>
            <div class="mini-box"><div class="mini-label">Distanz</div><div class="mini-value">{formatiere_entfernung(evaluation.entfernung_km)}</div></div>
            <div class="mini-box"><div class="mini-label">Distanzfaktor</div><div class="mini-value">{formatiere_faktor(referenz.get('distanzfaktor', 1.0))}</div></div>
        </div>
        <div class="hint-line">Format: <strong>{referenz['formatklasse']}</strong> · Demo-Distanzlogik: <strong>{referenz.get('distanzhinweis', 'nicht bewertet')}</strong></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
