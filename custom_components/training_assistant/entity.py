"""Gemeinsame Basis für alle Entitäten: ein Gerät „TrainingAssistant ‹Name›“ pro Person."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL_PERSON_ADDED, SIGNAL_UPDATE, VERSION
from .manager import TrainingManager


def person_device_id(entry_id: str, pid: str) -> tuple[str, str]:
    """Kennung des Geräts einer Person."""
    return (DOMAIN, f"{entry_id}_{pid}")


@callback
def setup_person_entities(hass: HomeAssistant, entry: ConfigEntry, async_add_entities,
                          factory: Callable[[TrainingManager], Iterable[Entity]]) -> None:
    """Entitäten für jede Person anlegen – auch für Personen, die später dazukommen."""
    hub = entry.runtime_data
    async_add_entities([e for m in hub.persons.values() for e in factory(m)])

    @callback
    def added(pid: str) -> None:
        if pid in hub.persons:
            async_add_entities(list(factory(hub.persons[pid])))

    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_PERSON_ADDED, added))


class TrainingEntity(Entity):
    """Hängt am Gerät der Person und aktualisiert sich bei jeder Änderung."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, manager: TrainingManager, key: str) -> None:
        self.manager = manager
        self._attr_unique_id = f"{manager.entry.entry_id}_{manager.pid}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={person_device_id(manager.entry.entry_id, manager.pid)},
            name=f"TrainingAssistant {manager.profile['name']}",
            entry_type=DeviceEntryType.SERVICE,
            sw_version=VERSION,
        )

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(async_dispatcher_connect(self.hass, SIGNAL_UPDATE, self._handle_update))

    @callback
    def _handle_update(self) -> None:
        self.async_write_ha_state()

    @property
    def current_step(self) -> dict | None:
        active = self.manager.active
        if not active:
            return None
        idx = active["idx"]
        return active["steps"][idx] if 0 <= idx < len(active["steps"]) else None
