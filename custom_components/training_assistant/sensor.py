"""Sensoren: Status, aktuelle Übung, Fortschritt, letzter Satz."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TrainingConfigEntry
from .const import SET_SKIPPED
from .phrases import Speech
from .entity import TrainingEntity, setup_person_entities

STATUS_OPTIONS = ["idle", "ready", "active", "interval", "paused"]


async def async_setup_entry(
    hass: HomeAssistant, entry: TrainingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    setup_person_entities(hass, entry, async_add_entities, lambda m: [
        StatusSensor(m, "status"), ExerciseSensor(m, "current_exercise"), ProgressSensor(m, "progress"),
        LastSetSensor(m, "last_set"), WeekSensor(m, "workouts_this_week"), StreakSensor(m, "streak")])


class StatusSensor(TrainingEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = STATUS_OPTIONS

    @property
    def native_value(self) -> str:
        active = self.manager.active
        if not active:
            return "idle"
        if active["paused"]:
            return "paused"
        return active["phase"] if active["phase"] in STATUS_OPTIONS else "idle"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        active = self.manager.active
        if not active:
            return {"next_workout": self.manager.data.get("next")}
        return {
            "plan": active["plan_name"],
            "workout": active["workout_name"],
            "session_id": active["id"],
            "step": active["idx"] + 1,
            "total_steps": len(active["steps"]),
            "sets_logged": len([s for s in active["sets"] if s["status"] != SET_SKIPPED]),
            "satellite": active.get("satellite"),
            "started_at": active["started_at"],
            "pending_question": active.get("pending_question"),
        }


class ExerciseSensor(TrainingEntity, SensorEntity):
    _attr_icon = "mdi:dumbbell"

    @property
    def native_value(self) -> str | None:
        step = self.current_step
        if not step:
            return None
        if step["type"] == "set":
            return step["exercise_name"]
        interval = (self.manager.active or {}).get("interval")
        if step["type"] == "interval" and interval and interval.get("exercise"):
            return interval["exercise"]
        return Speech(self.manager.active.get("lang", "de")).block_name(step)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        step = self.current_step
        if not step:
            return {}
        active = self.manager.active
        steps = active["steps"]
        nxt = next((s for s in steps[step["idx"] + 1:] if s["type"] == "set"), None)
        return {
            "block": step["block_name"],
            "block_type": step["block_type"],
            "position": Speech(active.get("lang", "de")).position(step) if step["type"] == "set" else None,
            "target_reps": step.get("target_reps"),
            "rep_range": step.get("rep_range"),
            "target_weight": step.get("target_weight"),
            "target_duration": step.get("target_duration") or step.get("duration_s"),
            "suggestion": step.get("suggestion"),
            "note": step.get("note"),
            "next_exercise": nxt["exercise_name"] if nxt else None,
            "rest_until": active.get("rest_until"),
            "interval": active.get("interval"),
        }


class ProgressSensor(TrainingEntity, SensorEntity):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:progress-check"

    @property
    def native_value(self) -> int | None:
        active = self.manager.active
        if not active:
            return None
        return round(100 * active["idx"] / max(1, len(active["steps"])))


class LastSetSensor(TrainingEntity, SensorEntity):
    _attr_icon = "mdi:clipboard-check-outline"

    def _last(self) -> dict | None:
        active = self.manager.active
        if active and active["sets"]:
            return active["sets"][-1]
        return None

    @property
    def native_value(self) -> str | None:
        rec = self._last()
        if not rec:
            return None
        if rec["status"] == SET_SKIPPED:
            return f"{rec['exercise_name']}: {Speech(self.manager.active.get('lang', 'de')).t('skipped').rstrip('.')}"
        if rec.get("duration_s") and rec.get("reps") is None:
            value = f"{rec['duration_s']} s"
        else:
            value = f"{rec.get('reps')}"
            if rec.get("weight_kg") is not None:
                value += f" × {Speech(self.manager.active.get('lang', 'de')).number(rec['weight_kg'])} kg"
        return f"{rec['exercise_name']}: {value}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        rec = self._last()
        return dict(rec) if rec else {}


class WeekSensor(TrainingEntity, SensorEntity):
    """Trainings in dieser Woche (Mo–So) der aktiven Person; Ziel als Attribut."""

    _attr_icon = "mdi:calendar-week"
    _attr_native_unit_of_measurement = "workouts"

    @property
    def native_value(self) -> int:
        return self.manager.week_info()["done"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        info = self.manager.week_info()
        return {"goal": info["goal"], "left": max(0, info["goal"] - info["done"]), "total": info["total"],
                "person": self.manager.profile["name"]}


class StreakSensor(TrainingEntity, SensorEntity):
    """Wochen am Stück mit erreichtem Wochenziel."""

    _attr_icon = "mdi:fire"
    _attr_native_unit_of_measurement = "weeks"

    @property
    def native_value(self) -> int:
        return self.manager.week_info()["streak_weeks"]
