"""TrainingAssistant: Trainingspläne abarbeiten und Sätze per Knopf/Sprache erfassen.

Die Integration kennt bewusst keine Hardware. Knöpfe und Sprach-Satelliten docken
über Automationen bzw. Blueprints an die Entitäten und Aktionen dieser Integration an.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.typing import ConfigType

from .errors import error
from .const import CARD_FILENAME, CARD_URL, DOMAIN, GUIDE_URL, IMAGES_DIR, IMAGES_URL, SIGNAL_UPDATE, VERSION
from .manager import TrainingManager
from .services import async_setup_services
from .websocket import async_setup_websocket

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.CALENDAR, Platform.NUMBER, Platform.SELECT, Platform.SENSOR]

type TrainingConfigEntry = ConfigEntry[TrainingManager]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Einmalig: Aktionen, Websocket-Befehle und Dashboard-Karte registrieren."""
    async_setup_services(hass)
    async_setup_websocket(hass)
    card = Path(__file__).parent / "frontend" / CARD_FILENAME
    image_dir = Path(hass.config.path(IMAGES_DIR))
    await hass.async_add_executor_job(lambda: image_dir.mkdir(parents=True, exist_ok=True))
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(CARD_URL, str(card), False),
            # Übungsbilder: einmal geladen, ändern sich nicht → darf der Browser cachen
            StaticPathConfig(IMAGES_URL, str(image_dir), True),
            # Anleitung und Beispielplan für eigene Pläne (Download in der Karte)
            StaticPathConfig(GUIDE_URL, str(Path(__file__).parent / "guide"), False),
        ]
    )
    # Prüfsumme in der Adresse: Nach einem Update lädt der Browser die neue Karte statt der alten aus dem Cache
    digest = await hass.async_add_executor_job(_file_digest, card)
    add_extra_js_url(hass, f"{CARD_URL}?v={VERSION}-{digest}")
    return True


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


async def async_setup_entry(hass: HomeAssistant, entry: TrainingConfigEntry) -> bool:
    """Integration aus einem Konfigurationseintrag einrichten."""
    manager = TrainingManager(hass, entry)
    await manager.async_load()
    entry.runtime_data = manager
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    return True


async def _async_options_updated(hass: HomeAssistant, entry: TrainingConfigEntry) -> None:
    """Optionen geändert: Entitäten und Karte neu zeichnen (Optionen werden live gelesen)."""
    async_dispatcher_send(hass, SIGNAL_UPDATE)


async def async_unload_entry(hass: HomeAssistant, entry: TrainingConfigEntry) -> bool:
    """Integration entladen."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_unload()
    return unloaded


def get_manager(hass: HomeAssistant) -> TrainingManager:
    """Den Manager der (einzigen) geladenen Instanz holen."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        manager = getattr(entry, "runtime_data", None)
        if isinstance(manager, TrainingManager):
            return manager
    raise error("not_set_up")
