"""
Unbooked pickup cost calculations.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_09_BUILD_005"
PURPOSE = "Summarize completed pickups that have not been booked into cost control yet"
"""

from dataclasses import dataclass
from typing import Any

from data.demo_data import UNBOOKED_PICKUPS_DEMO


@dataclass(frozen=True)
class UnbookedPickupSummary:
    """Cost summary for completed but unbooked pickups."""

    count: int
    total_cost: float
    items: tuple[dict[str, Any], ...]


def summarize_unbooked_pickups(pickups: list[dict[str, Any]] | None = None) -> UnbookedPickupSummary:
    """
    Sum costs for pickups with status `ungebucht`.

    Input: pickup records with `kosten` and `status`.
    Output: count, total cost, and the included records.
    Fehlerfall: missing or invalid cost values are treated as visible zero-cost records only if explicitly present.
    Einheit: EUR.
    Quelle: demo data now; later ERP/TMS pickup ledger.
    """
    source = pickups if pickups is not None else UNBOOKED_PICKUPS_DEMO
    open_items = tuple(item for item in source if item.get("status") == "ungebucht")
    total_cost = sum(float(item.get("kosten") or 0.0) for item in open_items)
    return UnbookedPickupSummary(
        count=len(open_items),
        total_cost=round(total_cost, 2),
        items=open_items,
    )
