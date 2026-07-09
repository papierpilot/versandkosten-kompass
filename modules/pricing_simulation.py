"""
Simulation pricing and recommendation helpers.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_001"
PURPOSE = "Calculate simulated provider prices and recommendation metrics"
"""

from data.demo_data import ANBIETER_MODELLE
from modules.location_demo import berechne_demo_distanzfaktor, formatiere_faktor
from modules.shipping_rules import (
    berechne_gurtmass,
    berechne_mengenfaktor,
    berechne_simulations_dynamik,
    berechne_volumen_gewicht,
    ermittle_ausschlussgruende,
    ermittle_formatklasse,
)


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
