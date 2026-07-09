"""
Shipment data contracts for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_002"
PURPOSE = "Typed input and evaluation objects for the shipping workflow"
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ShipmentInput:
    """User-entered shipment data before provider evaluation."""

    paket_menge: int
    gewicht_kg: float
    laenge_cm: float
    breite_cm: float
    hoehe_cm: float
    empfaenger: str
    land: str
    plz: str
    ort: str


@dataclass(frozen=True)
class ShipmentEvaluation:
    """Complete result of one shipment evaluation run."""

    input_data: ShipmentInput
    plz_norm: str
    entfernung_km: int | None
    entfernung_hinweis: str
    ergebnisse: list[dict[str, Any]]
    bestes_ergebnis: dict[str, Any] | None
    referenz: dict[str, Any]
    warnungen: list[str]
    zulaessig_gesamt: int
    ausgeschlossen_gesamt: int
    vertrauensscore: int
    ersparnis_betrag: float
    ersparnis_prozent: float
    teuerster_anbieter: dict[str, Any] | None
