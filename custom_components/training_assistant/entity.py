"""Gemeinsame Basis für alle Entitäten."""

from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL_UPDATE, VERSION
from .manager import TrainingManager


class TrainingEntity(Entity):
    """Hängt am Gerät „TrainingAssistant“ und aktualisiert sich bei jeder Änderung."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, manager: TrainingManager, key: str) -> None:
        self.manager = manager
        self._attr_unique_id = f"{manager.entry.entry_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, manager.entry.entry_id)},
            name="TrainingAssistant",
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
