"""
Provider comparison rendering.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_22_BUILD_008"
PURPOSE = "Render provider comparison HTML from prepared evaluation results"
"""

from modules.pricing_simulation import begruendung_fuer_anbieter, euro


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
        if ergebnis.get("deadline_status") and ergebnis.get("deadline_status") != "nicht_bewertet":
            begruendung = f"{begruendung} · Zustellfrist: {ergebnis.get('deadline_service', '-')}"
        cells.extend([
            f"<div class='provider-cell'><span class='rank'>{index}</span></div>",
            f"<div class='provider-cell'><strong>{ergebnis['anbieter']}</strong>{empfehlung}<div class='provider-sub'>{ergebnis['formatklasse']}</div></div>",
            f"<div class='provider-cell price-cell'>{preis}</div>",
            f"<div class='provider-cell'>{status}<div class='provider-reason'>{begruendung}</div></div>",
        ])
    return f"<div class='provider-grid'>{''.join(cells)}</div>"
