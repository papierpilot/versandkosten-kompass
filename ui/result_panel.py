"""
Recommendation and booking panels for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_22_BUILD_008"
PURPOSE = "Render recommendation, decision context, and simulated booking from prepared data"
"""

import time

import streamlit as st

from data.demo_data import ANBIETER_MODELLE, VERSANDSTANDORT
from modules.location_demo import formatiere_entfernung, formatiere_faktor
from modules.pricing_simulation import entscheidungsbasis_html, euro
from modules.shipment_model import ShipmentEvaluation
from services.booking_service import build_booking
from services.label_pdf import make_demo_label_pdf


def build_decision_note(evaluation: ShipmentEvaluation) -> str:
    """Build the visible decision note from a prepared evaluation."""
    shipment = evaluation.input_data
    sender = shipment.sender_profile()
    bestes_ergebnis = evaluation.bestes_ergebnis
    if not bestes_ergebnis:
        return "Keine zulässige Empfehlung. Maße oder Gewicht müssen geprüft werden."

    deadline_sentence = ""
    if evaluation.deadline_result and evaluation.deadline_result.get("status") != "nicht_bewertet":
        deadline_sentence = (
            f" Zustellfrist: {evaluation.deadline_result['anforderung']} "
            f"({evaluation.deadline_result['ziel']})."
        )

    return (
        f"Alle Anbieter geprüft · {evaluation.zulaessig_gesamt} zulässig · "
        f"{evaluation.ausgeschlossen_gesamt} ausgeschlossen. "
        f"Empfehlung: {bestes_ergebnis['anbieter']}, weil günstigster zulässiger Anbieter bei "
        f"{shipment.effective_paket_menge} Paket(en) und {evaluation.referenz['abrechnungsgewicht']:.2f} kg Abrechnungsgewicht. "
        f"Ziel: {shipment.plz or 'ohne PLZ'} {shipment.ort or ''}, {shipment.land}. "
        f"Demo-Entfernung ab {sender.plz} {sender.ort}: "
        f"{formatiere_entfernung(evaluation.entfernung_km)}. "
        f"Distanzfaktor: {formatiere_faktor(bestes_ergebnis.get('distanzfaktor', 1.0))} "
        f"({bestes_ergebnis.get('distanzhinweis', 'nicht bewertet')})."
        f"{deadline_sentence}"
    )


def render_result_panel(evaluation: ShipmentEvaluation) -> bool:
    """Render result column and return whether productive display mode is active."""
    shipment = evaluation.input_data
    sender = shipment.sender_profile()
    bestes_ergebnis = evaluation.bestes_ergebnis
    referenz = evaluation.referenz

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
                    {shipment.effective_paket_menge} Paket(e) · {euro(bestes_ergebnis['preis_pro_paket'])} pro Paket<br>
                    {bestes_ergebnis['formatklasse']} · {referenz['abrechnungsgewicht']:.2f} kg Abrechnung / Paket<br>
                    Versand ab {sender.plz} {sender.ort} · {formatiere_entfernung(evaluation.entfernung_km)}<br>
                    Distanzfaktor {formatiere_faktor(bestes_ergebnis.get('distanzfaktor', 1.0))} · {bestes_ergebnis.get('distanzhinweis', 'nicht bewertet')}<br>
                    Zustellprofil: {bestes_ergebnis.get('deadline_service', 'nicht geprüft')} · {bestes_ergebnis.get('deadline_reason', 'keine Zustellfrist angegeben')}<br>
                    {bestes_ergebnis['demo_hinweis']}
                </div>
                <div class="trust-list">
                    {entscheidungsbasis_html(bestes_ergebnis, shipment.effective_paket_menge, evaluation.entfernung_km)}
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
            st.session_state["booking"] = build_booking(
                bestes_ergebnis,
                shipment.effective_paket_menge,
                shipment.total_gewicht_kg,
                evaluation.referenz["paket_details"][0]["laenge_cm"],
                evaluation.referenz["paket_details"][0]["breite_cm"],
                evaluation.referenz["paket_details"][0]["hoehe_cm"],
                shipment.empfaenger,
                shipment.land,
                shipment.plz,
                shipment.ort,
                evaluation.entfernung_km,
            )
    else:
        st.error("Kein Anbieter kann diese Sendung im aktuellen Simulationsmodell abbilden.")
    st.markdown('</div>', unsafe_allow_html=True)

    if evaluation.deadline_result and evaluation.deadline_result.get("status") != "nicht_bewertet":
        deadline = evaluation.deadline_result
        services = "<br>".join(deadline.get("top_services") or [deadline.get("hinweis", "Keine fristgerechte Option im Demo-Profil.")])
        box_class = "ok-box" if deadline.get("status") == "erfuellbar" else "warning-box"
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Zustellfrist</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="message-box {box_class}">
                <strong>{deadline['ziel']}</strong><br>
                Anforderung: {deadline['anforderung']} · Verfügbare Tage: {deadline['tage_verfuegbar']}<br>
                {services}
                <div class="hint-line">{deadline['hinweis']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if bestes_ergebnis:
        teuerster_name = evaluation.teuerster_anbieter["anbieter"] if evaluation.teuerster_anbieter else "—"
        teuerster_preis = euro(evaluation.teuerster_anbieter["preis"]) if evaluation.teuerster_anbieter else "—"
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Nutzen & Vertrauen</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="mini-grid">
                <div class="mini-box"><div class="mini-label">Ersparnis</div><div class="mini-value">{euro(evaluation.ersparnis_betrag)}</div></div>
                <div class="mini-box"><div class="mini-label">Gegen {teuerster_name}</div><div class="mini-value">{evaluation.ersparnis_prozent:.1f} %</div></div>
                <div class="mini-box"><div class="mini-label">Manuell</div><div class="mini-value">ca. 10 min</div></div>
                <div class="mini-box"><div class="mini-label">System</div><div class="mini-value">&lt; 3 sek</div></div>
                <div class="mini-box"><div class="mini-label">Vertrauen</div><div class="mini-value">{evaluation.vertrauensscore} %</div></div>
                <div class="mini-box"><div class="mini-label">Geprüft</div><div class="mini-value">{len(ANBIETER_MODELLE)} Anbieter</div></div>
            </div>
            <div class="hint-line">Teuerster zulässiger Anbieter: {teuerster_preis}. Zeitwerte sind Demo-Annahmen und werden später mit realer Ist-Zeit ersetzt.</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Entscheidungsnotiz</div>', unsafe_allow_html=True)
    note = build_decision_note(evaluation)
    if bestes_ergebnis:
        st.markdown(f"<div class='message-box ok-box'>{note}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-box warning-box'>{note}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if bestes_ergebnis:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Entscheidungssicherheit</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="message-box ok-box">
                <div class="trust-percent">{evaluation.vertrauensscore} %</div>
                <div>Die Empfehlung basiert auf geprüften Sendungsdaten, Anbietergrenzen, Preislogik und Demo-Distanzbewertung.</div>
                <div class="hint-line">{len(ANBIETER_MODELLE)} Anbieter geprüft · {evaluation.zulaessig_gesamt} zulässig · {evaluation.ausgeschlossen_gesamt} ausgeschlossen</div>
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

    return produktivmodus
