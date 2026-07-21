"""
Simulation pricing and recommendation helpers.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_006"
PURPOSE = "Calculate simulated provider prices and recommendation metrics"
"""

from data.demo_data import ANBIETER_MODELLE
from modules.shipment_model import PackageItem
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


def _package_metrics(package: PackageItem) -> dict:
    volumen_gewicht = berechne_volumen_gewicht(package.laenge_cm, package.breite_cm, package.hoehe_cm)
    abrechnungsgewicht = max(package.gewicht_kg, volumen_gewicht)
    formatklasse = ermittle_formatklasse(
        package.laenge_cm,
        package.breite_cm,
        package.hoehe_cm,
        abrechnungsgewicht,
    )
    return {
        "position": package.position,
        "gewicht_kg": package.gewicht_kg,
        "laenge_cm": package.laenge_cm,
        "breite_cm": package.breite_cm,
        "hoehe_cm": package.hoehe_cm,
        "volumengewicht": volumen_gewicht,
        "abrechnungsgewicht": abrechnungsgewicht,
        "formatklasse": formatklasse,
        "max_kante": max(package.laenge_cm, package.breite_cm, package.hoehe_cm),
        "gurtmass": berechne_gurtmass(package.laenge_cm, package.breite_cm, package.hoehe_cm),
    }


def _dominant_formatklasse(metrics: list[dict]) -> str:
    rank = {
        "Standardpaket": 1,
        "Standardpaket schwer": 2,
        "Großpaket": 3,
        "Sperrgut": 4,
        "Stückgut / Spedition": 5,
    }
    return max((item["formatklasse"] for item in metrics), key=lambda name: rank.get(name, 0))


def _package_surcharges(modell_name: str, formatklasse: str, abrechnungsgewicht: float, paket_menge: int) -> list[tuple[str, float]]:
    zuschlaege = []
    if formatklasse == "Großpaket":
        zuschlaege.append(("Großpaket", 6.50))
    elif formatklasse == "Sperrgut":
        zuschlaege.append(("Sperrgut", 18.00))
    elif formatklasse == "Stückgut / Spedition":
        zuschlaege.append(("Stückgut", 39.00))
    if modell_name == "Cargoboard" and formatklasse == "Stückgut / Spedition":
        zuschlaege.append(("Speditionsvorteil", -12.00))
    if modell_name == "Zipmend" and paket_menge >= 3:
        zuschlaege.append(("Mengenimpuls", -2.00))
    if modell_name == "Jumingo" and paket_menge >= 2:
        zuschlaege.append(("Plattformbündelung", -1.20))
    if modell_name == "UPS" and abrechnungsgewicht > 31.5:
        zuschlaege.append(("Schwerpaket", 9.50))
    return zuschlaege


def simuliere_anbieterpreise_fuer_pakete(packages, entfernung_km=None):
    package_items = tuple(packages)
    if not package_items:
        raise ValueError("Mindestens ein Paket muss für die Preisermittlung vorhanden sein.")

    paket_menge = len(package_items)
    package_metrics = [_package_metrics(package) for package in package_items]
    gesamt_volumengewicht = sum(item["volumengewicht"] for item in package_metrics)
    gesamt_abrechnungsgewicht = sum(item["abrechnungsgewicht"] for item in package_metrics)
    gesamt_realgewicht = sum(item["gewicht_kg"] for item in package_metrics)
    max_abrechnungsgewicht = max(item["abrechnungsgewicht"] for item in package_metrics)
    max_kante = max(item["max_kante"] for item in package_metrics)
    max_gurtmass = max(item["gurtmass"] for item in package_metrics)
    formatklasse = _dominant_formatklasse(package_metrics)
    mengenfaktor, mengenhinweis = berechne_mengenfaktor(paket_menge)
    distanzfaktor, distanzhinweis = berechne_demo_distanzfaktor(entfernung_km)
    ergebnisse = []

    for modell in ANBIETER_MODELLE:
        ausschlussgruende = []
        for item in package_metrics:
            item_gruende = ermittle_ausschlussgruende(
                modell,
                item["abrechnungsgewicht"],
                item["max_kante"],
                item["gurtmass"],
                item["formatklasse"],
            )
            for grund in item_gruende:
                ausschlussgruende.append(f"Paket {item['position']}: {grund}")

        paketpreise = []
        zuschlag_namen = []
        for item in package_metrics:
            basis = modell["basis"]
            gewichtskosten = item["abrechnungsgewicht"] * modell["kg"]
            handling = modell["handling"]
            zuschlaege = _package_surcharges(
                modell["name"],
                item["formatklasse"],
                item["abrechnungsgewicht"],
                paket_menge,
            )
            zuschlag_namen.extend(name for name, _ in zuschlaege)
            preis_vor_staffel = basis + gewichtskosten + handling + sum(wert for _, wert in zuschlaege)
            paketpreise.append(preis_vor_staffel)

        simulations_faktor, simulations_hinweis = berechne_simulations_dynamik(modell["name"], paket_menge)
        gesamtpreis = max(sum(paketpreise) * mengenfaktor * simulations_faktor * distanzfaktor, 0)
        preis_pro_paket = gesamtpreis / paket_menge
        moeglich = len(ausschlussgruende) == 0

        preisaufbau = [
            f"{paket_menge} Einzelpaket(e) bewertet",
            f"Gesamt Abrechnung {gesamt_abrechnungsgewicht:.2f} kg",
            f"Staffel {mengenfaktor:.2f}: {mengenhinweis}",
            f"Distanz {formatiere_faktor(distanzfaktor)}: {distanzhinweis}",
            f"Demo {simulations_faktor:.2f}: {simulations_hinweis}",
        ]
        for name in sorted(set(zuschlag_namen)):
            preisaufbau.append(f"Zuschlag: {name}")

        ergebnisse.append({
            "anbieter": modell["name"],
            "preis": round(gesamtpreis, 2),
            "preis_pro_paket": round(preis_pro_paket, 2),
            "moeglich": moeglich,
            "profil": modell["profil"],
            "formatklasse": formatklasse,
            "abrechnungsgewicht": max_abrechnungsgewicht,
            "gesamt_abrechnungsgewicht": gesamt_abrechnungsgewicht,
            "gesamt_realgewicht": gesamt_realgewicht,
            "volumengewicht": gesamt_volumengewicht,
            "gurtmass": max_gurtmass,
            "max_kante": max_kante,
            "paket_menge": paket_menge,
            "paket_details": package_metrics,
            "ausschlussgruende": ausschlussgruende,
            "preisaufbau": preisaufbau,
            "demo_hinweis": simulations_hinweis,
            "distanzfaktor": distanzfaktor,
            "distanzhinweis": distanzhinweis,
        })

    return sorted(ergebnisse, key=lambda x: (not x["moeglich"], x["preis"]))


def simuliere_anbieterpreise(paket_menge, gewicht_kg, laenge_cm, breite_cm, hoehe_cm, entfernung_km=None):
    packages = tuple(
        PackageItem(
            position=index,
            gewicht_kg=gewicht_kg,
            laenge_cm=laenge_cm,
            breite_cm=breite_cm,
            hoehe_cm=hoehe_cm,
        )
        for index in range(1, paket_menge + 1)
    )
    return simuliere_anbieterpreise_fuer_pakete(packages, entfernung_km)
