"""Auswertungen: Rekorde, Woche, Serie, Muskelvolumen, Erholung."""

from collections import Counter
from datetime import date, datetime, timedelta, timezone

from custom_components.training_assistant.progression import suggest
from custom_components.training_assistant.stats import (
    e1rm,
    muscle_volume,
    new_record,
    recovery,
    streak_weeks,
    week_start,
    week_summary,
)

TODAY = date(2026, 11, 6)  # Freitag


def _set(ex="squat", reps=8, w=50.0, status="confirmed", effort=None):
    return {"exercise": ex, "reps": reps, "weight_kg": w, "duration_s": None, "status": status, "effort": effort}


def _sess(day: date, sets, hour=18, minutes=45, name="A"):
    start = datetime(day.year, day.month, day.day, hour, tzinfo=timezone.utc)
    return {"id": f"{day}{hour}", "started_at": start.isoformat(),
            "finished_at": (start + timedelta(minutes=minutes)).isoformat(), "workout_name": name, "sets": sets}


def local_day(iso):
    return datetime.fromisoformat(iso).date()


def groups(rec, sess):
    return {"squat": ["quads", "glutes"], "bench": ["chest", "triceps"], "row": ["back"]}.get(rec["exercise"], [])


def test_e1rm():
    assert e1rm(100, 1) == 100 and e1rm(100, 10) == 133.3 and e1rm(100, 20) is None and e1rm(None, 5) is None


def test_new_record():
    prev = [_set(w=50, reps=8), _set(w=50, reps=8)]
    assert new_record(_set(w=52.5, reps=8), prev)["kind"] == "weight"
    assert new_record(_set(w=50, reps=10), prev)["kind"] == "e1rm"
    assert new_record(_set(w=50, reps=8), prev) is None
    assert new_record(_set(w=60), []) is None  # erstes Mal: kein Rekord
    assert new_record(_set(w=60, status="unconfirmed"), prev) is None
    bw = [_set(ex="push", w=None, reps=12)]
    assert new_record(_set(ex="push", w=None, reps=15), bw) == {"kind": "reps", "value": 15, "previous": 12}


def test_week_summary():
    mon = week_start(TODAY)
    sessions = [
        _sess(mon, [_set("squat")] * 3),
        _sess(mon + timedelta(days=1), [_set("bench")] * 4),
        _sess(mon + timedelta(days=3), [_set("row"), _set("row", status="skipped")]),
        _sess(mon - timedelta(days=2), [_set("squat")]),  # Vorwoche
    ]
    wk = week_summary(sessions, TODAY, local_day, groups, goal=4)
    assert (wk["done"], wk["left"], wk["goal"]) == (3, 1, 4)
    states = [d["state"] for d in wk["days"]]
    assert states == ["done", "done", "missed", "done", "today", "future", "future"]
    assert wk["days"][0]["sets"] == 3 and wk["days"][0]["groups"] == ["quads", "glutes"]
    assert wk["days"][3]["sets"] == 1  # übersprungener Satz zählt nicht


def test_streak():
    wk = week_start(TODAY)
    per = Counter({wk: 1, wk - timedelta(days=7): 3, wk - timedelta(days=14): 3, wk - timedelta(days=21): 1})
    assert streak_weeks(per, TODAY, 3) == 2  # laufende Woche (noch nicht erreicht) unterbricht nicht
    per[wk] = 3
    assert streak_weeks(per, TODAY, 3) == 3
    assert streak_weeks(Counter(), TODAY, 3) == 0


def test_muscle_volume_and_recovery():
    mon = week_start(TODAY)
    sessions = [_sess(mon, [_set("squat")] * 3), _sess(mon - timedelta(days=5), [_set("bench")] * 2)]
    vol = muscle_volume(sessions, TODAY, local_day, groups)
    assert vol["quads"] == {"week": 3, "last_week": 0} and vol["chest"] == {"week": 0, "last_week": 2}
    now = datetime(2026, 11, 6, 12, tzinfo=timezone.utc)
    rec = {r["group"]: r["status"] for r in recovery(sessions, now, groups, {"quads", "chest", "back"})}
    assert rec["quads"] == "ready"  # Montag 18:45 → Freitag 12:00 ≈ 89 h
    assert rec["chest"] == "overdue" and rec["back"] == "none"


def test_streak_uses_goal_of_each_week():
    from custom_components.training_assistant.stats import goal_for_week

    wk = week_start(TODAY)
    per = Counter({wk: 4, wk - timedelta(days=7): 3, wk - timedelta(days=14): 3})
    # Ziel war 3, ab dieser Woche 4 → frühere Wochen mit 3 Trainings zählen weiter
    history = {"1970-01-05": 3, wk.isoformat(): 4}
    assert streak_weeks(per, TODAY, lambda w: goal_for_week(history, w, 4)) == 3
    assert streak_weeks(per, TODAY, 4) == 1  # alt: alles am aktuellen Ziel gemessen
    assert goal_for_week({}, wk, 5) == 5


def test_time_average_only_over_trained_weeks():
    from custom_components.training_assistant.stats import time_stats

    mon = week_start(TODAY)
    only_now = [_sess(mon, [_set()], minutes=60)]
    assert time_stats(only_now, TODAY, local_day) == {"week_min": 60, "avg_min": None}
    two_weeks = only_now + [_sess(mon - timedelta(days=7), [_set()], minutes=40),
                            _sess(mon - timedelta(days=14), [_set()], minutes=20)]
    assert time_stats(two_weeks, TODAY, local_day)["avg_min"] == 30  # (40 + 20) / 2, nicht / 4


def test_recovery_levels():
    mon = week_start(TODAY)
    now = datetime(mon.year, mon.month, mon.day, 18, 45, tzinfo=timezone.utc)
    def status(hours):
        sess = _sess(mon, [_set("bench")], hour=18, minutes=45)
        return recovery([sess], now + timedelta(hours=hours), groups, set())[0]["status"]
    assert [status(h) for h in (5, 30, 60, 6 * 24, 9 * 24)] == ["fresh", "recovering", "ready", "soon", "overdue"]
