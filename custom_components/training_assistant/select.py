"""Auswahl: aktives Programm und nächstes Workout darin."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TrainingConfigEntry
from .entity import TrainingEntity, setup_person_entities


async def async_setup_entry(
    hass: HomeAssistant, entry: TrainingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    # Keine Auswahl „Person“ mehr: jede Person hat ihr eigenes Gerät
    setup_person_entities(hass, entry, async_add_entities,
                          lambda m: [ProgramSelect(m, "program"), NextWorkoutSelect(m, "next_workout")])


class ProgramSelect(TrainingEntity, SelectEntity):
    """Programm, in dem man sich bewegt. Wechseln = dort weitermachen, wo man war."""

    _attr_icon = "mdi:notebook-outline"

    @property
    def options(self) -> list[str]:
        return [p["name"] for p in self.manager.data["plans"].values()]

    @property
    def current_option(self) -> str | None:
        plan = self.manager.data["plans"].get(self.manager.data.get("program"))
        return plan["name"] if plan else None

    @property
    def available(self) -> bool:
        return bool(self.manager.data["plans"])

    async def async_select_option(self, option: str) -> None:
        for p in self.manager.data["plans"].values():
            if p["name"] == option:
                self.manager.set_program(p["id"])
                return


class NextWorkoutSelect(TrainingEntity, SelectEntity):
    """Nächstes Workout im aktiven Programm."""

    _attr_icon = "mdi:clipboard-list-outline"

    @property
    def options(self) -> list[str]:
        return [w["label"] for w in self.manager.program_workouts()]

    @property
    def current_option(self) -> str | None:
        nxt = self.manager.data.get("next")
        for w in self.manager.program_workouts():
            if nxt and w["workout_id"] == nxt["workout_id"]:
                return w["label"]
        return None

    @property
    def available(self) -> bool:
        return bool(self.manager.program_workouts())

    async def async_select_option(self, option: str) -> None:
        nxt = self.manager.data.get("next")
        for w in self.manager.program_workouts():
            if w["label"] == option and nxt:
                self.manager.set_next(nxt["plan_id"], w["workout_id"])
                return
