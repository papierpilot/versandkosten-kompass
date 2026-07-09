"""
API configuration status.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_001"
PURPOSE = "Read local provider API configuration without exposing secrets"
"""

import json
from pathlib import Path

from config.app_settings import API_CONFIG_FILE
from data.demo_data import ANBIETER_MODELLE


def lade_api_status(config_path: str | Path = API_CONFIG_FILE):
    """
    Preparation for real provider integrations.

    Real credentials stay in the local config file, Streamlit secrets, or environment variables.
    This function only reports whether a provider is marked enabled.
    """
    status = {modell["name"]: False for modell in ANBIETER_MODELLE}
    path = Path(config_path)

    if not path.exists():
        return status, "Keine lokale API-Datei gefunden. Simulationsmodus aktiv."

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return status, f"API-Datei vorhanden, aber JSON ist ungültig: {exc}"
    except OSError as exc:
        return status, f"API-Datei vorhanden, aber nicht lesbar: {exc}"

    for name in status:
        status[name] = bool(data.get(name.lower(), {}).get("enabled", False))
    return status, "Lokale API-Datei gefunden. Echte API-Aufrufe sind in dieser Version noch deaktiviert."
