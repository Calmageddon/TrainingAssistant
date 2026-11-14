"""Gemeinsame Testfälle mit Hero Upgrade: dieselben Eingaben müssen in Python dasselbe ergeben wie in TypeScript.

Die Fälle erzeugt Hero Upgrade (`npm run cases` → tests/fixtures/shared_cases.json). Schlägt hier etwas fehl, rechnen
die beiden Apps unterschiedlich – dann die falsche Seite korrigieren, nicht die Datei von Hand ändern.
"""

import json
from pathlib import Path

import pytest

from custom_components.training_assistant.plan import build_steps, parse_plan_text, slugify
from custom_components.training_assistant.progression import suggest, suggest_duration
from custom_components.training_assistant.stats import e1rm, groups_for, new_record, recovery_tier

ROOT = Path(__file__).resolve().parent.parent
CASES = json.loads((ROOT / "tests" / "fixtures" / "shared_cases.json").read_text(encoding="utf-8"))
TEMPLATES = ROOT / "custom_components" / "training_assistant" / "templates"


def _norm(v):
    """JSON-Vergleich: Tupel → Listen, 5.0 == 5 (TypeScript kennt nur „number“)."""
    if isinstance(v, dict):
        return {k: _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, float):
        return round(v, 6)
    return v


def _pick(d: dict, keys) -> dict:
    return {k: d.get(k) for k in keys}


@pytest.mark.parametrize("case", CASES["suggest"], ids=lambda c: c["name"])
def test_suggest(case):
    i = case["input"]
    rr = tuple(i["rep_range"]) if i["rep_range"] else None
    got = suggest(i["last_sets"], rep_range=rr, progression=i["progression"], plan_weight=i["plan_weight"])
    assert _norm(_pick(got, case["expect"])) == _norm(case["expect"]), i


@pytest.mark.parametrize("case", CASES["suggest_duration"], ids=lambda c: c["name"])
def test_suggest_duration(case):
    i = case["input"]
    got = suggest_duration(i["last_sets"], plan_duration=i["plan_duration"], plan_weight=i["plan_weight"], fixed=i["fixed"])
    assert _norm(_pick(got, case["expect"])) == _norm(case["expect"]), i


def test_small_functions():
    for c in CASES["e1rm"]:
        assert _norm(e1rm(*c["input"])) == _norm(c["expect"]), c
    for c in CASES["recovery_tier"]:
        assert recovery_tier(c["input"]) == c["expect"], c
    for c in CASES["groups_for"]:
        assert groups_for(c["input"]) == c["expect"], c
    for c in CASES["slugify"]:
        assert slugify(c["input"]) == c["expect"], c


@pytest.mark.parametrize("case", CASES["new_record"], ids=lambda c: str(c["input"]["rec"]))
def test_new_record(case):
    got = new_record(case["input"]["rec"], case["input"]["previous"])
    assert _norm(got) == _norm(case["expect"])


@pytest.mark.parametrize("case", CASES["build_steps"], ids=lambda c: f"{c['template']}:{c['workout']}")
def test_build_steps(case):
    plan = parse_plan_text((TEMPLATES / case["template"]).read_text(encoding="utf-8"))
    steps = build_steps(plan, case["workout"])
    assert len(steps) == len(case["expect"])
    for n, (got, want) in enumerate(zip(steps, case["expect"])):
        mine = {k: got.get(k) for k in want if k != "segments"}
        if "segments" in want:
            mine["segments"] = [{k: g.get(k) for k in w} for g, w in zip(got.get("segments") or [], want["segments"])]
        assert _norm(mine) == _norm(want), f"Schritt {n}"
        # Felder, die Python zusätzlich setzt, die TypeScript aber nicht kennt, sind erlaubt – fehlende nicht
