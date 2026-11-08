"""Mitgelieferte Vorlagen: gültig, zerlegbar, (fast) alle mit Bild."""

from pathlib import Path

import pytest

from custom_components.training_assistant.images import Catalog, map_plan
from custom_components.training_assistant.plan import build_steps, parse_plan_text

TEMPLATES = sorted((Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant"
                    / "templates").glob("*.yaml"))
CAT = Catalog.load()


def test_templates_exist():
    assert len(TEMPLATES) >= 16
    groups = {p.stem.split("-", 1)[0] for p in TEMPLATES}
    assert groups == {"kraft", "bodyweight", "calisthenics", "kettlebell"}


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.stem)
def test_template_valid(path):
    plan = parse_plan_text(path.read_text(encoding="utf-8"))
    for w in plan["workouts"]:
        assert build_steps(plan, w["id"])
    mapping = map_plan(plan, CAT)
    explicit = {k: ex["image"] for k, ex in plan["exercises"].items() if isinstance(ex.get("image"), str)}
    assert all(cid in CAT.by_id for cid in explicit.values()), explicit
    # bewusst ohne Bild (image: false) zählt nicht; sonst höchstens eine Übung ohne Bild
    wanted = [k for k, ex in plan["exercises"].items() if ex.get("image") is not False]
    assert sum(1 for k in wanted if mapping[k]) >= len(wanted) - 1


def test_template_names_unique():
    names = [parse_plan_text(p.read_text(encoding="utf-8"))["name"] for p in TEMPLATES]
    assert len(names) == len(set(names))
