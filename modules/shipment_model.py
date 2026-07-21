"""
Shipment data contracts for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_006"
PURPOSE = "Typed input and evaluation objects for single- and multi-package shipments"
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PackageItem:
    """One physical package in a shipment."""

    position: int
    gewicht_kg: float
    laenge_cm: float
    breite_cm: float
    hoehe_cm: float


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
    packages: tuple[PackageItem, ...] = ()

    def package_items(self) -> tuple[PackageItem, ...]:
        """Return explicit package items, or expand the uniform quick input."""
        if self.packages:
            return self.packages
        return tuple(
            PackageItem(
                position=index,
                gewicht_kg=self.gewicht_kg,
                laenge_cm=self.laenge_cm,
                breite_cm=self.breite_cm,
                hoehe_cm=self.hoehe_cm,
            )
            for index in range(1, self.paket_menge + 1)
        )

    @property
    def effective_paket_menge(self) -> int:
        """Number of physical packages considered by the workflow."""
        return len(self.package_items())

    @property
    def total_gewicht_kg(self) -> float:
        """Total real weight across all package items."""
        return round(sum(package.gewicht_kg for package in self.package_items()), 2)


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
