"""Tasten: Start, Weiter, Rückgängig, Pause, Überspringen, Beenden, Abbrechen.

Ein Zigbee-Knopf „drückt“ diese Tasten über eine Automation/Blueprint.
"""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TrainingConfigEntry
from .const import REST_STEP_S
from .entity import TrainingEntity

BUTTONS = ("start", "next", "undo", "pause", "skip", "finish", "abort")
# Plus/Minus für den laufenden Satz – z. B. für einen Drehregler
ADJUST_BUTTONS = {"reps_up": ("reps", 1), "reps_down": ("reps", -1), "weight_up": ("weight", 1),
                  "weight_down": ("weight", -1)}
# Pausentimer verlängern/verkürzen
REST_BUTTONS = {"rest_longer": REST_STEP_S, "rest_shorter": -REST_STEP_S}


async def async_setup_entry(
    hass: HomeAssistant, entry: TrainingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities([
        *(TrainingButton(entry.runtime_data, key) for key in BUTTONS),
        *(AdjustButton(entry.runtime_data, key) for key in ADJUST_BUTTONS),
        *(RestButton(entry.runtime_data, key) for key in REST_BUTTONS),
    ])


class TrainingButton(TrainingEntity, ButtonEntity):
    async def async_press(self) -> None:
        m = self.manager
        await {
            "start": m.async_start,
            "next": m.async_next,
            "undo": m.async_undo,
            "pause": m.async_pause,
            "skip": m.async_skip,
            "finish": m.async_finish,
            "abort": m.async_abort,
        }[self._attr_translation_key]()

    @property
    def available(self) -> bool:
        key = self._attr_translation_key
        if key == "start":
            return self.manager.active is None and bool(self.manager.data.get("next"))
        if key == "next":
            return self.manager.active is not None or bool(self.manager.data.get("next"))
        return self.manager.active is not None


class AdjustButton(TrainingEntity, ButtonEntity):
    """Wdh./Gewicht des laufenden Satzes um einen Schritt ändern (bei Zeit-Sätzen: ±5 s)."""

    async def async_press(self) -> None:
        field, steps = ADJUST_BUTTONS[self._attr_translation_key]
        self.manager.async_adjust(field, steps)

    @property
    def available(self) -> bool:
        adj = self.manager.adjust_state()
        if adj is None:
            return False
        if self._attr_translation_key.startswith("weight"):
            return adj["weight"] is not None
        return True


class RestButton(TrainingEntity, ButtonEntity):
    """Pause um 15 Sekunden verlängern bzw. verkürzen."""

    async def async_press(self) -> None:
        self.manager.async_rest_adjust(REST_BUTTONS[self._attr_translation_key])

    @property
    def available(self) -> bool:
        return self.manager.active is not None
