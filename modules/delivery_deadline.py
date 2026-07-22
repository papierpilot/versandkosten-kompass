"""
Delivery deadline evaluation for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_22_BUILD_009"
PURPOSE = "Pure service-level simulation for customer delivery deadlines"
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from modules.shipment_model import ShipmentInput


@dataclass(frozen=True)
class ProviderDeadlineProfile:
    """Service-level assumptions for one simulated provider."""

    standard_days: int
    express_days: int | None
    express_label: str


PROVIDER_DEADLINE_PROFILES: dict[str, ProviderDeadlineProfile] = {
    "DHL": ProviderDeadlineProfile(standard_days=2, express_days=None, express_label="Standard"),
    "UPS": ProviderDeadlineProfile(standard_days=2, express_days=1, express_label="UPS Express"),
    "Zipmend": ProviderDeadlineProfile(standard_days=2, express_days=1, express_label="Zipmend Express/Kurier"),
    "Jumingo": ProviderDeadlineProfile(standard_days=2, express_days=1, express_label="Jumingo Express-Option"),
    "Cargoboard": ProviderDeadlineProfile(standard_days=3, express_days=None, express_label="Standard"),
    "General Overnight": ProviderDeadlineProfile(standard_days=1, express_days=0, express_label="General Overnight Kurier"),
}


def _parse_deadline_date(raw_value: str) -> date | None:
    if not raw_value:
        return None
    try:
        return date.fromisoformat(raw_value)
    except ValueError:
        return None


def _evaluate_provider(ergebnis: dict[str, Any], days_available: int) -> dict[str, Any]:
    profile = PROVIDER_DEADLINE_PROFILES.get(ergebnis["anbieter"])
    annotated = dict(ergebnis)

    if not profile:
        annotated.update(
            deadline_ok=False,
            deadline_status="nicht_bewertet",
            deadline_service="Service-Level unbekannt",
            deadline_reason="Für diesen Anbieter ist noch kein Zustellprofil gepflegt.",
            deadline_rank=90,
        )
        return annotated

    if not ergebnis["moeglich"]:
        annotated.update(
            deadline_ok=False,
            deadline_status="ausgeschlossen",
            deadline_service="-",
            deadline_reason="Anbieter ist bereits durch Maß-, Gewichts- oder Tarifgrenzen ausgeschlossen.",
            deadline_rank=99,
        )
        return annotated

    if days_available < 0:
        annotated.update(
            deadline_ok=False,
            deadline_status="verpasst",
            deadline_service="nicht mehr erreichbar",
            deadline_reason="Der gewünschte Zustelltermin liegt in der Vergangenheit.",
            deadline_rank=98,
        )
    elif profile.express_days is not None and days_available >= profile.express_days:
        annotated.update(
            deadline_ok=True,
            deadline_status="express_ok" if days_available > 0 else "kurier_ok",
            deadline_service=profile.express_label,
            deadline_reason=f"Express-/Kurieroption im Demo-Profil: {profile.express_days} Werktag(e).",
            deadline_rank=4 if days_available == 0 else 5,
        )
    elif days_available == 0:
        annotated.update(
            deadline_ok=False,
            deadline_status="kurier_noetig",
            deadline_service="Same-Day/Kurier prüfen",
            deadline_reason="Für Zustellung am selben Tag wird ein tarifierter Kurierdienst benötigt.",
            deadline_rank=80,
        )
    elif days_available >= profile.standard_days:
        annotated.update(
            deadline_ok=True,
            deadline_status="standard_ok",
            deadline_service="Standard",
            deadline_reason=f"Standardlaufzeit im Demo-Profil: {profile.standard_days} Werktag(e).",
            deadline_rank=10,
        )
    else:
        annotated.update(
            deadline_ok=False,
            deadline_status="zu_langsam",
            deadline_service="nicht fristgerecht",
            deadline_reason="Das gepflegte Demo-Serviceprofil erfüllt die Zustellfrist nicht.",
            deadline_rank=70,
        )

    return annotated


def evaluate_delivery_deadline(
    shipment: ShipmentInput,
    provider_results: list[dict[str, Any]],
    today: date | None = None,
) -> dict[str, Any]:
    """
    Annotate provider results with simulated delivery deadline fit.

    Data contract:
    - Input: ShipmentInput plus already priced provider results.
    - Output: dictionary with annotated results and visible decision summary.
    - Fehlerfall: Missing or invalid deadline remains visible and does not crash workflow.
    - Einheit: Calendar date ISO-8601, days as whole calendar days.
    - Zeitbezug: Local system date unless tests pass a fixed date.
    - Quelle: Static demo service-level table in this module.
    """
    target_date = _parse_deadline_date(shipment.gewuenschtes_zustelldatum)
    if not target_date:
        return {
            "status": "nicht_bewertet",
            "ziel": "",
            "tage_verfuegbar": None,
            "anforderung": "keine Zustellfrist angegeben",
            "hinweis": "Ohne Zustelltermin bleibt die Empfehlung rein preis- und regelbasiert.",
            "ergebnisse": provider_results,
            "top_services": [],
        }

    reference_date = today or date.today()
    days_available = (target_date - reference_date).days
    annotated_results = [_evaluate_provider(ergebnis, days_available) for ergebnis in provider_results]
    deadline_sorted = sorted(
        annotated_results,
        key=lambda item: (
            not item.get("deadline_ok", False),
            item.get("deadline_rank", 99),
            not item.get("moeglich", False),
            item.get("preis", 999999),
        ),
    )
    feasible = [item for item in deadline_sorted if item.get("moeglich") and item.get("deadline_ok")]

    if days_available < 0:
        status = "kritisch"
        requirement = "Termin liegt in der Vergangenheit"
        hint = "Die Sendung kann diesen Termin nicht mehr erreichen."
    elif days_available == 0 and feasible:
        status = "erfuellbar"
        requirement = "Same-Day/Kurier erforderlich"
        hint = "General Overnight ist als Kurierprofil vorbereitet; Preise bleiben bis zur Preisliste Demo-Werte."
    elif days_available == 0:
        status = "kritisch"
        requirement = "Same-Day/Kurier erforderlich"
        hint = "Ein tarifierter Kurierdienst wird benötigt."
    elif feasible:
        status = "erfuellbar"
        requirement = "Express erforderlich" if days_available == 1 else "Standard voraussichtlich ausreichend"
        hint = f"{len(feasible)} Anbieter erfüllen die Zustellfrist im Demo-Serviceprofil."
    else:
        status = "nicht_erfuellbar"
        requirement = "kein gepflegtes Serviceprofil erfüllt die Frist"
        hint = "Für echte Zusagen müssen Provider-SLAs oder Kurierpreise angebunden werden."

    target_time = shipment.gewuenschte_zustellzeit or "Tagesende"
    return {
        "status": status,
        "ziel": f"{target_date.isoformat()} bis {target_time}",
        "tage_verfuegbar": days_available,
        "anforderung": requirement,
        "hinweis": hint,
        "ergebnisse": deadline_sorted,
        "top_services": [
            f"{item['anbieter']}: {item.get('deadline_service', '-')}" for item in feasible[:3]
        ],
    }
