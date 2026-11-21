"""Sicherung im gemeinsamen Format mit Hero Upgrade (backup.py) – geprüft mit einer echten HU-Sicherung.

tests/fixtures/hu_backup_sample.json erzeugt Hero Upgrade (`npm run cases`): ein Training-Verlauf im neuen Format
(portable) und dasselbe als alte HU-Sicherung (legacy).
"""

import copy
import json
from pathlib import Path

import pytest

from custom_components.training_assistant import backup as bk
from custom_components.training_assistant.plan import validate_plan

SAMPLE = json.loads((Path(__file__).parent / "fixtures" / "hu_backup_sample.json").read_text(encoding="utf-8"))
NOW = "2026-11-15T10:00:00+00:00"


def test_reads_hu_backup_and_old_hu_format():
    new = bk.normalize(SAMPLE["portable"], NOW)
    old = bk.normalize(SAMPLE["legacy"], NOW)
    for b in (new, old):
        assert b["format"] == bk.BACKUP_FORMAT
        assert [p["name"] for p in b["people"]] == ["Dom"]
        assert len(b["people"][0]["sessions"]) == 2
        assert b["plans"] and all(not validate_plan({**p["data"], "schema_version": 1}) for p in b["plans"])
    assert [s["id"] for s in old["people"][0]["sessions"]] == [s["id"] for s in new["people"][0]["sessions"]]


def test_rejects_other_files():
    for bad in ({}, {"hallo": 1}, {"format": "training-log", "plans": [], "people": [{"id": 1}]}, []):
        with pytest.raises(bk.BackupError):
            bk.normalize(bad, NOW)
    with pytest.raises(bk.BackupError) as err:
        bk.normalize({"format": "training-log", "version": 99, "plans": [], "people": []}, NOW)
    assert err.value.key == "backup_too_new"


def test_suggests_person_by_name_or_the_only_one():
    b = bk.normalize(SAMPLE["portable"], NOW)
    assert bk.summarize(b, {"dom": {"name": "dom"}, "anna": {"name": "Anna"}}, {})["people"][0]["suggestion"] == "dom"
    assert bk.summarize(b, {"p1": {"name": "Dominik"}}, {})["people"][0]["suggestion"] == "p1"  # je eine Person
    two = bk.summarize(b, {"p1": {"name": "Dominik"}, "p2": {"name": "Anna"}}, {})
    assert two["people"][0]["suggestion"] == "new" and two["plans_new"] == len(b["plans"])


def test_merge_adds_new_sessions_once():
    sessions = copy.deepcopy(SAMPLE["portable"]["people"][0]["sessions"])
    target: list = []
    assert bk.merge_sessions(target, sessions) == (2, 0)
    assert bk.merge_sessions(target, sessions) == (0, 2)  # noch einmal: nichts doppelt
    same_start = [{**sessions[0], "id": "andere_id"}]  # gleicher Start + Workout = dasselbe Training
    assert bk.merge_sessions(target, same_start) == (0, 1)
    assert [s["started_at"] for s in target] == sorted(s["started_at"] for s in target)


def test_export_roundtrip():
    b = bk.normalize(SAMPLE["portable"], NOW)
    plans = {p["id"]: {**p, "data": p["data"]} for p in b["plans"]}
    profiles = {p["id"]: {"id": p["id"], "name": p["name"], "weekly_goal": p["weekly_goal"]} for p in b["people"]}
    persons = {p["id"]: {"sessions": p["sessions"], "program": p["program"], "rotation": p["rotation"]} for p in b["people"]}
    out = bk.to_portable(plans, profiles, persons, app="training-assistant", app_version="x", now_iso=NOW)
    again = bk.normalize(json.loads(json.dumps(out)), NOW)
    assert again["app"] == "training-assistant"
    assert again["people"][0]["sessions"] == b["people"][0]["sessions"]
    assert [p["id"] for p in again["plans"]] == [p["id"] for p in b["plans"]]


def test_hero_data_of_hu_survives_import_and_export():
    """Heldenmodus-Daten aus HU (fertige Stories, Orden …) bleiben je Person erhalten und gehen beim Export wieder mit."""
    b = bk.normalize(SAMPLE["portable"], NOW)
    person = next(p for p in b["people"] if p.get("hero"))
    person["hero"]["runs"] = [{"story": "seven_minutes", "started_at": "2026-11-01T08:00:00Z", "finished_at": "2026-11-20T08:00:00Z"}]
    hero = bk.merge_hero({}, copy.deepcopy(person["hero"]))
    assert hero["runs"][0]["finished_at"] == "2026-11-20T08:00:00Z"  # fertige Story im Regal
    assert hero["badges"] == person["hero"]["badges"]
    profiles = {person["id"]: {"id": person["id"], "name": person["name"], "hero": hero}}
    out = bk.to_portable({}, profiles, {person["id"]: {"sessions": []}}, app="training-assistant", app_version="x", now_iso=NOW)
    again = bk.normalize(json.loads(json.dumps(out)), NOW)
    assert again["people"][0]["hero"] == hero
    # zweimal einlesen ändert nichts (nichts doppelt)
    assert bk.merge_hero(copy.deepcopy(hero), copy.deepcopy(person["hero"])) == hero
