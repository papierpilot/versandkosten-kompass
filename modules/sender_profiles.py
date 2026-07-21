"""
Sender profile selection and conversion helpers.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_21_BUILD_007"
PURPOSE = "Provide selectable sender profiles without embedding sender logic in the UI"
"""

from dataclasses import dataclass

from data.demo_data import SENDER_PROFILES, VERSANDSTANDORT


@dataclass(frozen=True)
class SenderProfile:
    """One selectable sender/origin address."""

    id: str
    name: str
    strasse: str
    plz: str
    ort: str
    land: str
    lat: float
    lon: float

    @property
    def display_name(self) -> str:
        return f"{self.name} · {self.plz} {self.ort}"

    @property
    def address_line(self) -> str:
        return f"{self.strasse} · {self.plz} {self.ort}"


def sender_from_dict(data: dict) -> SenderProfile:
    """Convert a static sender profile dictionary into a typed sender object."""
    return SenderProfile(
        id=str(data["id"]),
        name=str(data["name"]),
        strasse=str(data["strasse"]),
        plz=str(data["plz"]),
        ort=str(data["ort"]),
        land=str(data["land"]),
        lat=float(data["lat"]),
        lon=float(data["lon"]),
    )


def list_sender_profiles() -> tuple[SenderProfile, ...]:
    """Return all configured sender profiles."""
    return tuple(sender_from_dict(profile) for profile in SENDER_PROFILES)


def default_sender_profile() -> SenderProfile:
    """Return the default sender profile for backward-compatible workflow calls."""
    return sender_from_dict(VERSANDSTANDORT)


def find_sender_profile(sender_id: str) -> SenderProfile:
    """Find a sender profile by id, falling back to the default sender."""
    for sender in list_sender_profiles():
        if sender.id == sender_id:
            return sender
    return default_sender_profile()
