"""Kalender mit allen Trainings der aktiven Person (Monatsansicht in Home Assistant, Automationen)."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import TrainingConfigEntry
from .const import SET_SKIPPED
from .entity import TrainingEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: TrainingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities([TrainingCalendar(entry.runtime_data, "calendar")])


def _event(sess: dict) -> CalendarEvent:
    start = dt_util.parse_datetime(sess["started_at"])
    end = dt_util.parse_datetime(sess["finished_at"]) if sess.get("finished_at") else None
    if not end or end <= start:
        end = start + timedelta(minutes=1)
    done = [x for x in sess["sets"] if x["status"] != SET_SKIPPED]
    lines = []
    for rec in done:
        value = f"{rec.get('reps')}" if rec.get("reps") is not None else f"{rec.get('duration_s')} s"
        if rec.get("weight_kg") is not None:
            value += f" × {rec['weight_kg']:g} kg"
        lines.append(f"{rec['exercise_name']}: {value}")
    return CalendarEvent(
        start=start, end=end, summary=sess["workout_name"],
        description=f"{sess['plan_name']} · {len(done)} sets\n" + "\n".join(lines),
        uid=sess["id"],
    )


class TrainingCalendar(TrainingEntity, CalendarEntity):
    _attr_icon = "mdi:calendar-check"

    @property
    def event(self) -> CalendarEvent | None:
        """Laufendes Training, sonst das letzte."""
        active = self.manager.active
        if active:
            return _event({**active, "finished_at": dt_util.utcnow().isoformat()})
        sessions = self.manager.data["sessions"]
        return _event(sessions[-1]) if sessions else None

    async def async_get_events(self, hass: HomeAssistant, start_date: datetime, end_date: datetime) -> list[CalendarEvent]:
        out = []
        for sess in self.manager.data["sessions"]:
            ev = _event(sess)
            if ev.end > start_date and ev.start < end_date:
                out.append(ev)
        return out
