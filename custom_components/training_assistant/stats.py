"""Auswertungen über den Verlauf: Rekorde, Woche, Serie, Muskelvolumen, Erholung.

Ohne Home-Assistant-Abhängigkeiten. Der Manager liefert Sessions, die Zuordnung
Satz → Muskelgruppen und die Umrechnung in lokale Kalendertage.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from typing import Any, Callable

SKIPPED = "skipped"
UNCONFIRMED = "unconfirmed"
PENDING = "pending"

# Hauptmuskeln aus dem Übungskatalog → Muskelgruppen für Anzeige und Erholung
MUSCLE_GROUPS: dict[str, str] = {
    "chest": "chest",
    "lats": "back", "middle back": "back", "lower back": "back", "traps": "back",
    "shoulders": "shoulders",
    "biceps": "biceps", "forearms": "biceps",
    "triceps": "triceps",
    "abdominals": "core",
    "quadriceps": "quads", "adductors": "quads",
    "hamstrings": "hamstrings",
    "glutes": "glutes", "abductors": "glutes",
    "calves": "calves",
}
GROUP_ORDER = ["chest", "back", "shoulders", "biceps", "triceps", "core", "quads", "hamstrings", "glutes", "calves"]

# Erholung (Stunden seit dem letzten Training der Muskelgruppe)
FRESH_H = 24
RECOVERING_H = 48
TRAIN_SOON_H = 5 * 24
OVERDUE_H = 8 * 24


def counts(rec: dict) -> bool:
    """Satz zählt für Statistik (gemacht, mit Werten)."""
    return rec.get("status") not in (SKIPPED, PENDING) and (
        rec.get("reps") is not None or rec.get("duration_s") is not None)


def groups_for(muscles: list[str]) -> list[str]:
    out: list[str] = []
    for m in muscles:
        g = MUSCLE_GROUPS.get(m)
        if g and g not in out:
            out.append(g)
    return out


# ---------------------------------------------------------------------------
# Rekorde
# ---------------------------------------------------------------------------

def e1rm(weight: float | None, reps: int | None) -> float | None:
    """Geschätztes Maximalgewicht (Epley), nur für 1–12 Wdh. sinnvoll."""
    if not weight or not reps or reps < 1 or reps > 12:
        return None
    return round(weight * (1 + reps / 30), 1) if reps > 1 else float(weight)


def bests(sets: list[dict]) -> dict[str, float]:
    """Bestwerte einer Übung: weight (schwerstes Gewicht), e1rm, reps (meiste Wdh. ohne Gewicht), duration."""
    out: dict[str, float] = {}
    for rec in sets:
        if not counts(rec) or rec.get("status") == UNCONFIRMED:
            continue
        w, r, d = rec.get("weight_kg"), rec.get("reps"), rec.get("duration_s")
        if w:
            out["weight"] = max(out.get("weight", 0), w)
            est = e1rm(w, r)
            if est:
                out["e1rm"] = max(out.get("e1rm", 0), est)
        elif r is not None:
            out["reps"] = max(out.get("reps", 0), r)
        if d is not None and not w:
            out["duration"] = max(out.get("duration", 0), d)
    return out


def new_record(rec: dict, previous: list[dict]) -> dict[str, Any] | None:
    """Neuer Bestwert durch diesen Satz? Nur wenn es schon einen Vergleichswert gibt.

    Reihenfolge: Gewicht > geschätztes Maximum > Wiederholungen > Dauer (nur der wichtigste wird gemeldet).
    """
    old = bests(previous)
    new = bests([rec])
    for kind in ("weight", "e1rm", "reps", "duration"):
        if kind in new and kind in old and new[kind] > old[kind]:
            return {"kind": kind, "value": new[kind], "previous": old[kind]}
    return None


# ---------------------------------------------------------------------------
# Woche, Serie, Zeit
# ---------------------------------------------------------------------------

def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())  # Montag


def week_summary(
    sessions: list[dict],
    today: date,
    local_day: Callable[[str], date],
    groups_of: Callable[[dict, dict], list[str]],
    goal: int,
) -> dict[str, Any]:
    """Die aktuelle Woche (Mo–So): pro Tag Sätze und trainierte Muskelgruppen."""
    start = week_start(today)
    days = [{"date": (start + timedelta(days=i)).isoformat(), "sets": 0, "workouts": 0, "groups": Counter(),
             "names": []} for i in range(7)]
    for sess in sessions:
        d = local_day(sess["started_at"])
        if not start <= d < start + timedelta(days=7):
            continue
        day = days[(d - start).days]
        done = [x for x in sess["sets"] if counts(x)]
        if not done:
            continue
        day["workouts"] += 1
        day["names"].append(sess.get("workout_name"))
        day["sets"] += len(done)
        for rec in done:
            for g in groups_of(rec, sess):
                day["groups"][g] += 1
    for day in days:
        day["groups"] = [g for g, _ in day["groups"].most_common(2)]
        day["state"] = ("done" if day["workouts"] else
                        "today" if day["date"] == today.isoformat() else
                        "missed" if day["date"] < today.isoformat() else "future")
    done_count = sum(d["workouts"] for d in days)
    return {"start": start.isoformat(), "today": today.isoformat(), "goal": goal, "done": done_count,
            "left": max(0, goal - done_count), "days": days}


def weekly_counts(sessions: list[dict], local_day: Callable[[str], date]) -> Counter:
    """Anzahl Trainings je Wochenbeginn (nur Trainings mit mindestens einem Satz)."""
    out: Counter = Counter()
    for sess in sessions:
        if any(counts(x) for x in sess["sets"]):
            out[week_start(local_day(sess["started_at"]))] += 1
    return out


def goal_for_week(history: dict[str, int], week: date, current: int) -> int:
    """Wochenziel, das in dieser Woche galt: letzter Eintrag mit Wochenbeginn <= week, sonst das aktuelle."""
    valid = [k for k in history if k <= week.isoformat()]
    return history[max(valid)] if valid else current


def streak_weeks(per_week: Counter, today: date, goal: int | Callable[[date], int]) -> int:
    """Wochen am Stück, in denen das Wochenziel erreicht wurde.

    goal: festes Ziel oder Funktion Wochenbeginn → Ziel dieser Woche (Ziele können sich ändern,
    jede Woche wird an ihrem damaligen Ziel gemessen).
    Die laufende Woche zählt mit, sobald das Ziel erreicht ist; sonst unterbricht sie die Serie nicht.
    """
    goal_of = goal if callable(goal) else (lambda _w: goal)
    week = week_start(today)
    streak = 1 if per_week.get(week, 0) >= max(1, goal_of(week)) else 0
    week -= timedelta(days=7)
    while per_week.get(week, 0) >= max(1, goal_of(week)):
        streak += 1
        week -= timedelta(days=7)
    return streak


def duration_min(sess: dict) -> float:
    try:
        start = datetime.fromisoformat(sess["started_at"])
        end = datetime.fromisoformat(sess["finished_at"])
    except (KeyError, TypeError, ValueError):
        return 0.0
    # Pausen (Knopf „Pause“) zählen nicht zur Trainingszeit
    return max(0.0, ((end - start).total_seconds() - (sess.get("paused_s") or 0)) / 60)


def time_stats(sessions: list[dict], today: date, local_day: Callable[[str], date], weeks: int = 4) -> dict:
    """Trainingszeit diese Woche und Durchschnitt der letzten abgeschlossenen Wochen (Minuten).

    Gemittelt wird nur über Wochen seit dem ersten Training (höchstens `weeks`); gibt es noch keine
    abgeschlossene Woche, ist avg_min None.
    """
    this_week = week_start(today)
    per_week: Counter = Counter()
    for sess in sessions:
        per_week[week_start(local_day(sess["started_at"]))] += duration_min(sess)
    first = min(per_week) if per_week else this_week
    past = [this_week - timedelta(days=7 * i) for i in range(1, weeks + 1)]
    past = [w for w in past if w >= first]
    avg = round(sum(per_week.get(w, 0.0) for w in past) / len(past)) if past else None
    return {"week_min": round(per_week.get(this_week, 0.0)), "avg_min": avg}


# ---------------------------------------------------------------------------
# Muskelgruppen: Wochenvolumen und Erholung
# ---------------------------------------------------------------------------

def muscle_volume(
    sessions: list[dict],
    today: date,
    local_day: Callable[[str], date],
    groups_of: Callable[[dict, dict], list[str]],
) -> dict[str, dict[str, int]]:
    """Harte Sätze pro Muskelgruppe: diese Woche und letzte Woche."""
    this_week = week_start(today)
    last_week = this_week - timedelta(days=7)
    out: dict[str, dict[str, int]] = {}
    for sess in sessions:
        wk = week_start(local_day(sess["started_at"]))
        if wk not in (this_week, last_week):
            continue
        key = "week" if wk == this_week else "last_week"
        for rec in sess["sets"]:
            if not counts(rec):
                continue
            for g in groups_of(rec, sess):
                out.setdefault(g, {"week": 0, "last_week": 0})[key] += 1
    return out


# Vorsprung sekundär trainierter Muskelgruppen: zählen, als wäre das Training so viele Stunden früher gewesen
# (direkt danach höchstens „erholt sich“, nach einem Tag bereit).
SECONDARY_HEAD_START_H = 24


def recovery(
    sessions: list[dict],
    now: datetime,
    groups_of: Callable[[dict, dict], list[str]],
    relevant: set[str],
    secondary_of: Callable[[dict, dict], list[str]] | None = None,
) -> list[dict[str, Any]]:
    """Erholungsstatus je Muskelgruppe: fresh (<24 h) / recovering (<48 h) / ready / soon / overdue (nie: none).

    groups_of = primäre Gruppen (zählen voll), secondary_of = sekundäre (mit SECONDARY_HEAD_START_H Vorsprung).
    """
    last: dict[str, datetime] = {}

    def note(g: str, t: datetime) -> None:
        if g not in last or t > last[g]:
            last[g] = t

    head_start = timedelta(hours=SECONDARY_HEAD_START_H)
    for sess in sessions:
        try:
            when = datetime.fromisoformat(sess.get("finished_at") or sess["started_at"])
        except (KeyError, TypeError, ValueError):
            continue
        for rec in sess["sets"]:
            if not counts(rec):
                continue
            for g in groups_of(rec, sess):
                note(g, when)
            if secondary_of:
                for g in secondary_of(rec, sess):
                    note(g, when - head_start)
    out = []
    for g in GROUP_ORDER:
        if g not in relevant and g not in last:
            continue
        if g not in last:
            out.append({"group": g, "status": "none", "hours": None})
            continue
        hours = (now - last[g]).total_seconds() / 3600
        status = ("fresh" if hours < FRESH_H else "recovering" if hours < RECOVERING_H else "ready" if hours < TRAIN_SOON_H
                  else "soon" if hours < OVERDUE_H else "overdue")
        out.append({"group": g, "status": status, "hours": round(hours)})
    return out
