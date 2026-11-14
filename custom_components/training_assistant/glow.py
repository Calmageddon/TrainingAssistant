"""Lichtsignal: Phase des Trainings als Farbe einer RGB-Lampe (wie der Leuchtrand in Hero Upgrade).

  work  = grün (Satz/Arbeitsphase läuft)        rest = gelb (Pause, Seitenwechsel, HIIT-Pause)
  count = rot (letzte COUNT_S Sekunden vor „Los“, Countdown vor einem Satz nach Zeit)
  wait  = rot, gedämpft (wartet auf „Los“)      off  = Lampe wie vor dem Training (pausiert, Training vorbei)
Beim Wechsel aus Pause/Countdown in die Arbeit leuchtet die Lampe kurz mit voller Helligkeit, bei einem Rekord golden.
Ohne HA-Abhängigkeit.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

COUNT_S = 3
COLORS: dict[str, tuple[int, int, int]] = {
    "work": (0, 230, 118),
    "rest": (255, 190, 0),
    "count": (255, 23, 68),
    "wait": (229, 57, 53),
    "record": (255, 200, 40),
}
# Helligkeit (0–255): dauerhaft gedämpft, beim Wechsel in die Arbeit, im Countdown und beim Rekord voll
BRIGHT_SOFT = 150
BRIGHT_FULL = 255
BURST_S = 2.0
RECORD_S = 3.0


def _left(iso: str | None, now: datetime) -> float | None:
    if not iso:
        return None
    try:
        return (datetime.fromisoformat(iso) - now).total_seconds()
    except (TypeError, ValueError):
        return None


def _until(active: dict[str, Any]) -> tuple[str | None, bool]:
    """Ende des laufenden Zeitabschnitts und ob davor rot gezählt wird."""
    iv = active.get("interval") if active.get("phase") == "interval" else None
    if iv and iv.get("ends_at"):
        return iv["ends_at"], iv.get("phase") != "work"
    if active.get("rest_until"):
        return active["rest_until"], True
    hold = active.get("hold")
    if hold and hold.get("phase") == "switch":
        return hold.get("until"), True
    return None, False


def glow_state(active: dict[str, Any] | None, now: datetime) -> str:
    """Farbzustand der Lampe für den aktuellen Trainingszustand."""
    if not active or active.get("paused"):
        return "off"
    iv = active.get("interval") if active.get("phase") == "interval" else None
    if iv and iv.get("ends_at"):
        if iv.get("phase") == "work":
            return "work"
        left = _left(iv["ends_at"], now)
        return "count" if left is not None and left <= COUNT_S else "rest"
    if active.get("rest_until"):
        left = _left(active["rest_until"], now)
        return "count" if left is not None and left <= COUNT_S else "rest"
    hold = active.get("hold")
    if hold and active.get("phase") == "active":
        if hold.get("phase") == "ready":
            return "count"  # Countdown vor einem Satz nach Zeit
        if hold.get("phase") == "switch":
            left = _left(hold.get("until"), now)
            return "count" if left is not None and left <= COUNT_S else "rest"
        return "work"
    if active.get("phase") == "ready":
        return "wait"  # wartet auf „Los“
    return "work" if active.get("phase") == "active" else "off"


def seconds_to_count(active: dict[str, Any] | None, now: datetime) -> float | None:
    """Sekunden bis zum Wechsel auf „count“ (rot) – für einen Timer; None = kein Wechsel absehbar."""
    if not active or active.get("paused"):
        return None
    until, counts = _until(active)
    left = _left(until, now) if counts else None
    if left is None or left <= COUNT_S:
        return None
    return left - COUNT_S
