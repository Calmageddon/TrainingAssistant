"""Anleitungen und Beispielpläne für eigene Pläne (Englisch und Deutsch): gültig und aktuell."""

import importlib.util
from pathlib import Path

import pytest

from custom_components.training_assistant.plan import build_steps, parse_plan_text

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "custom_components" / "training_assistant" / "guide"
CARD = ROOT / "custom_components" / "training_assistant" / "frontend" / "training-assistant-card.js"


def _builder():
    spec = importlib.util.spec_from_file_location("build_guide", ROOT / "tools" / "build_guide.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", ["example-plan.yaml", "beispiel-plan.yaml"])
def test_example_plan_valid_and_uses_all_block_types(name):
    plan = parse_plan_text((GUIDE / name).read_text(encoding="utf-8"))
    types = {b["type"] for w in plan["workouts"] for b in w["blocks"]}
    assert types == {"warmup", "sets", "circuit", "interval", "cooldown"}
    for w in plan["workouts"]:
        assert build_steps(plan, w["id"])


@pytest.mark.parametrize("lang", ["en", "de"])
def test_guide_is_up_to_date(lang):
    builder = _builder()
    target = builder.LANGS[lang][2]
    assert target.read_text(encoding="utf-8") == builder.build(lang), \
        "Anleitung veraltet – bitte .venv/bin/python tools/build_guide.py ausführen"


@pytest.mark.parametrize(
    ("name", "prompt", "mistakes"),
    [
        ("guide-custom-plans.txt", "Create a training plan for me in the YAML format", "Common mistakes"),
        ("anleitung-eigene-plaene.txt", "Erstelle mir einen Trainingsplan im YAML-Format", "Häufige Fehler"),
    ],
)
def test_guide_contains_prompt_and_example(name, prompt, mistakes):
    text = (GUIDE / name).read_text(encoding="utf-8")
    assert prompt in text
    assert "schema_version: 1" in text and mistakes in text


def test_card_offers_existing_guide_files():
    """Die Karte verlinkt je Sprache Anleitung und Beispiel – die Dateien müssen existieren."""
    import re

    card = CARD.read_text(encoding="utf-8")
    files = set(re.findall(r'(?:guide_file|example_file): "([^"]+)"', card))
    assert len(files) == 4
    for f in files:
        assert (GUIDE / f).exists(), f
