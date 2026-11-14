"""Zahlen: Wiederholungen und Gewicht des laufenden Satzes (für Hardware mit Wertausgabe)."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import UnitOfMass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TrainingConfigEntry
from .entity import TrainingEntity, setup_person_entities


async def async_setup_entry(
    hass: HomeAssistant, entry: TrainingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    setup_person_entities(hass, entry, async_add_entities,
                          lambda m: [RepsNumber(m, "set_reps"), WeightNumber(m, "set_weight")])


class RepsNumber(TrainingEntity, NumberEntity):
    """Wiederholungen – bei Zeit-Sätzen Sekunden."""

    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0
    _attr_native_max_value = 600
    _attr_native_step = 1
    _attr_icon = "mdi:counter"

    @property
    def available(self) -> bool:
        return self.manager.adjust_state() is not None

    @property
    def native_value(self) -> float | None:
        adj = self.manager.adjust_state()
        if adj is None:
            return None
        return adj["duration"] if adj["timed"] else adj["reps"]

    @property
    def native_unit_of_measurement(self) -> str | None:
        adj = self.manager.adjust_state()
        return "s" if adj and adj["timed"] else None

    async def async_set_native_value(self, value: float) -> None:
        self.manager.async_set_value("reps", value)


class WeightNumber(TrainingEntity, NumberEntity):
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0
    _attr_native_max_value = 500
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_icon = "mdi:weight-kilogram"

    @property
    def available(self) -> bool:
        adj = self.manager.adjust_state()
        return adj is not None and adj["weight"] is not None

    @property
    def native_step(self) -> float:
        adj = self.manager.adjust_state()
        return adj["weight_step"] if adj else 0.5

    @property
    def native_value(self) -> float | None:
        adj = self.manager.adjust_state()
        return adj["weight"] if adj else None

    async def async_set_native_value(self, value: float) -> None:
        self.manager.async_set_value("weight", value)
