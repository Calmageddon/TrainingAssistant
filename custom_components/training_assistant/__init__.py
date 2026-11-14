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
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.typing import ConfigType

from .errors import error
from .const import (CARD_FILENAME, CARD_URL, DOMAIN, GUIDE_URL, IMAGES_URL, SIGNAL_PERSON_REMOVED, SIGNAL_UPDATE,
                    VERSION)
from .entity import person_device_id
from .manager import TrainingHub, TrainingManager
from .services import async_setup_services
from .websocket import async_setup_websocket

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.CALENDAR, Platform.NUMBER, Platform.SELECT, Platform.SENSOR]

type TrainingConfigEntry = ConfigEntry[TrainingHub]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Einmalig: Aktionen, Websocket-Befehle und Dashboard-Karte registrieren."""
    async_setup_services(hass)
    async_setup_websocket(hass)
    card = Path(__file__).parent / "frontend" / CARD_FILENAME
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(CARD_URL, str(card), False),
            # Übungsbilder: mitgeliefert, ändern sich nur mit der Version (steht in der Adresse) → Cache erlaubt
            StaticPathConfig(IMAGES_URL, str(Path(__file__).parent / "pictos"), True),
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
    hub = TrainingHub(hass, entry)
    await hub.async_load()
    entry.runtime_data = hub
    devices = dr.async_get(hass)
    # Früher gab es ein gemeinsames Gerät für alle – jetzt eines pro Person
    old = devices.async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    if old:
        devices.async_remove_device(old.id)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    @callback
    def person_removed(pid: str) -> None:
        device = devices.async_get_device(identifiers={person_device_id(entry.entry_id, pid)})
        if device:
            devices.async_remove_device(device.id)

    @callback
    def names_changed() -> None:
        # Person umbenannt → Gerätename „TrainingAssistant ‹Name›“ nachziehen
        for pid, prof in hub.root["profiles"].items():
            device = devices.async_get_device(identifiers={person_device_id(entry.entry_id, pid)})
            name = f"TrainingAssistant {prof['name']}"
            if device and device.name != name:
                devices.async_update_device(device.id, name=name)

    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_PERSON_REMOVED, person_removed))
    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_UPDATE, names_changed))
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


def get_hub(hass: HomeAssistant) -> TrainingHub:
    """Die Zentrale der (einzigen) geladenen Instanz holen."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        hub = getattr(entry, "runtime_data", None)
        if isinstance(hub, TrainingHub):
            return hub
    raise error("not_set_up")
