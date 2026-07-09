"""
Shipping rule calculations.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_09_BUILD_005"
PURPOSE = "Pure package calculations, plausibility checks, and provider exclusion rules"
"""

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
        "Jumingo": [(2, 0.98, "Plattformpreis bei Einzelpaketen stabil"), (4, 0.90, "Vorteil bei kleinen Online-Buchungen"), (9, 0.93, "solide Plattformkondition bei Mischmengen"), (19, 0.97, "Mengen bleiben gut planbar"), (999999, 1.04, "Großmengen eher Speditionsprüfung")],
        "UPS": [(2, 1.08, "Einzelpaket nicht günstigstes Profil"), (4, 1.03, "noch kein deutlicher Vorteil"), (9, 0.78, "Vorteil bei mittleren Mengen"), (19, 0.92, "Mengenfenster bleibt interessant"), (999999, 1.00, "Großmengen neutral")],
        "Cargoboard": [(2, 1.30, "Spedition bei kleinen Mengen unattraktiv"), (4, 1.18, "noch zu geringe Bündelung"), (9, 1.02, "Schwelle zur Bündelung"), (19, 0.55, "Vorteil bei Sammelversand"), (999999, 0.34, "starker Vorteil bei Großmengen")],
    }
    for grenze, faktor, hinweis in matrix.get(anbieter_name, [(999999, 1.00, "neutral")]):
        if paket_menge <= grenze:
            return faktor, hinweis
    return 1.00, "neutral"
