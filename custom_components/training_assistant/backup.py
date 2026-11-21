"""Gemeinsames Sicherungsformat mit Hero Upgrade („training-log“), ohne HA-Abhängigkeit.

  { format: "training-log", version: 1, app, app_version, exported_at,
    plans:  [{ id, name, template, category, data }],
    people: [{ id, name, figure, weekly_goal, goal_history, program, rotation, sessions: [...], hero? }] }

hero (optional): Daten des Heldenmodus aus Hero Upgrade, die sich nicht aus dem Verlauf berechnen lassen (Story-Durchgänge
mit fertigen Stories, Orden-Daten, Figur, Stil …). TA hat (noch) keinen Heldenmodus, hebt sie aber je Person auf
(profile["hero"]), führt sie wie HU zusammen (merge_hero) und schreibt sie beim Export wieder mit – so geht nichts
verloren, und ein späterer Heldenmodus in TA findet das Regal mit fertigen Stories vor.

Gleiches Format wie Hero Upgrade (src/core/backup.ts) – so lässt sich der Verlauf per Datei zwischen HU und TA tauschen.
Sessions sind abgeschlossene Trainings mit allen Sätzen (gleicher Aufbau in beiden Apps), laufende gehören nie dazu.
Alte HU-Sicherungen ({app: "hero-upgrade", data}) werden beim Einlesen umgewandelt.
"""

from __future__ import annotations

import copy
from typing import Any

BACKUP_FORMAT = "training-log"
BACKUP_VERSION = 1


class BackupError(ValueError):
    """Ungültige Sicherung (key = Übersetzungsschlüssel)."""

    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key = key


def to_portable(plans: dict[str, Any], profiles: dict[str, Any], persons: dict[str, dict[str, Any]], *,
                app: str, app_version: str | None, now_iso: str) -> dict[str, Any]:
    """Speicher → gemeinsames Format. persons[pid] = Daten der Person (sessions, program, rotation …)."""
    return {
        "format": BACKUP_FORMAT, "version": BACKUP_VERSION, "app": app, "app_version": app_version,
        "exported_at": now_iso,
        "plans": [{"id": p["id"], "name": p["name"], "template": p.get("template"), "category": p.get("category"),
                   "data": copy.deepcopy(p["data"])} for p in plans.values()],
        "people": [{
            "id": prof["id"], "name": prof["name"], "figure": prof.get("figure"), "weekly_goal": prof.get("weekly_goal"),
            "goal_history": dict(prof["goal_history"]) if prof.get("goal_history") else None,
            "program": (persons.get(pid) or {}).get("program"),
            "rotation": dict((persons.get(pid) or {}).get("rotation") or {}),
            "sessions": copy.deepcopy((persons.get(pid) or {}).get("sessions") or []),
            **({"hero": copy.deepcopy(prof["hero"])} if prof.get("hero") else {}),
        } for pid, prof in profiles.items()],
    }


def merge_hero(target: dict[str, Any], incoming: Any) -> dict[str, Any]:
    """Helden-Daten ergänzen wie Hero Upgrade (mergeHero in src/core/backup.ts, gemeinsame Testfälle).

    Eigene Einstellungen bleiben; Story-Durchgänge kommen dazu (ein dort beendeter Durchgang gilt hier als beendet,
    höchstens eine aktive Story – eine weitere wird pausiert); bei Orden und Markierungen gilt das frühere Datum.
    """
    if not isinstance(incoming, dict):
        return target
    for k in ("on", "asked", "figure", "style", "alias"):
        if k not in target and k in incoming:
            target[k] = incoming[k]
    if target.get("runs") is None:
        target["runs"] = []
    runs: list[dict[str, Any]] = target["runs"]

    def active() -> bool:
        return any(not r.get("finished_at") and not r.get("paused_at") for r in runs)

    for r in incoming.get("runs") if isinstance(incoming.get("runs"), list) else []:
        if not isinstance(r, dict) or not isinstance(r.get("story"), str) or not r.get("started_at"):
            continue
        mine = next((x for x in runs if x.get("story") == r["story"] and x.get("started_at") == r["started_at"]), None)
        if mine is not None:
            if r.get("finished_at") and not mine.get("finished_at"):
                mine.update(copy.deepcopy(r))
            continue
        run = copy.deepcopy(r)
        run.pop("goal_prev", None)  # das Wochenziel dieses Geräts bleibt, wie es ist
        if not run.get("finished_at") and not run.get("paused_at") and active():
            run["paused_at"] = run["started_at"]  # nur eine aktive Story
        runs.append(run)
    runs.sort(key=lambda x: str(x.get("started_at")))
    for key in ("badges", "marks"):
        if target.get(key) is None:
            target[key] = {}
        t = target[key]
        for bid, date in (incoming.get(key) or {}).items():
            if isinstance(date, str) and (not t.get(bid) or date < t[bid]):
                t[bid] = date
    if incoming.get("power_pauses") and not target.get("power_pauses"):
        target["power_pauses"] = copy.deepcopy(incoming["power_pauses"])
    if (incoming.get("tutorial") or {}).get("done"):
        target.setdefault("tutorial", {})["done"] = True
    return target


def _legacy_hu(file: dict[str, Any], now_iso: str) -> dict[str, Any]:
    """Alte HU-Sicherung: aktive Person direkt in data, die anderen in data.profile_data."""
    data = file["data"]
    persons: dict[str, dict[str, Any]] = {}
    for pid in (data.get("profiles") or {}):
        persons[pid] = data if pid == data.get("profile") else (data.get("profile_data") or {}).get(pid) or {}
    return to_portable(data.get("plans") or {}, data.get("profiles") or {}, persons, app="hero-upgrade",
                       app_version=None, now_iso=file.get("exported_at") or now_iso)


def normalize(file: Any, now_iso: str) -> dict[str, Any]:
    """Datei prüfen und ins gemeinsame Format bringen. Wirft BackupError."""
    if isinstance(file, dict) and file.get("app") == "hero-upgrade" and isinstance(file.get("data"), dict) \
            and not file.get("format"):
        return _legacy_hu(file, now_iso)
    if not isinstance(file, dict) or file.get("format") != BACKUP_FORMAT \
            or not isinstance(file.get("plans"), list) or not isinstance(file.get("people"), list):
        raise BackupError("invalid_backup")
    try:
        version = int(file.get("version") or 0)
    except (TypeError, ValueError) as err:
        raise BackupError("invalid_backup") from err
    if version > BACKUP_VERSION:
        raise BackupError("backup_too_new")
    for p in file["people"]:
        if not isinstance(p, dict) or not isinstance(p.get("id"), str) or not isinstance(p.get("sessions"), list):
            raise BackupError("invalid_backup")
    for p in file["plans"]:
        if not isinstance(p, dict) or not isinstance(p.get("id"), str) or not isinstance(p.get("data"), dict):
            raise BackupError("invalid_backup")
    return file


def summarize(b: dict[str, Any], profiles: dict[str, Any], plans: dict[str, Any]) -> dict[str, Any]:
    """Inhalt und Vorschlag je Person der Datei: vorhandene Person mit gleichem Namen, sonst „new“
    (bei je genau einer Person auf beiden Seiten: diese)."""
    by_name = {str(p["name"]).strip().casefold(): pid for pid, p in profiles.items()}
    single = next(iter(profiles)) if len(profiles) == 1 and len(b["people"]) == 1 else None
    return {
        "app": b.get("app"), "exported_at": b.get("exported_at"), "plans": len(b["plans"]),
        "plans_new": sum(1 for p in b["plans"] if p["id"] not in plans),
        "people": [{"id": p["id"], "name": p.get("name") or "?", "sessions": len(p["sessions"]),
                    "suggestion": by_name.get(str(p.get("name") or "").strip().casefold()) or single or "new"}
                   for p in b["people"]],
    }


def _keys(s: dict[str, Any]) -> tuple[str, str]:
    return f"id:{s.get('id')}", f"at:{s.get('started_at')}|{s.get('workout_id')}"


def merge_sessions(target: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> tuple[int, int]:
    """Trainings ergänzen: nur neue (gleiche ID oder gleicher Start + Workout = schon da), nach Startzeit sortiert."""
    seen = {k for s in target for k in _keys(s)}
    added = skipped = 0
    for s in incoming:
        if not isinstance(s, dict) or not s.get("id") or not s.get("started_at") or any(k in seen for k in _keys(s)):
            skipped += 1
            continue
        target.append(copy.deepcopy(s))
        seen.update(_keys(s))
        added += 1
    target.sort(key=lambda s: str(s.get("started_at")))
    return added, skipped
