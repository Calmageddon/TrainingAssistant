"""Karte: Englisch und Deutsch haben dieselben Schlüssel, jeder Vorschlag ist übersetzt."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant"
CARD = (ROOT / "frontend" / "training-assistant-card.js").read_text(encoding="utf-8")


def _keys(lang: str) -> set[str]:
    block = re.search(rf"\n  {lang}: \{{\n(.*?)\n  \}},", CARD, re.S).group(1)
    # Schlüssel = Bezeichner direkt vor „: "“ (Texte selbst enthalten „Wort: {…}“, das zählt nicht)
    return set(re.findall(r'(?:^|[\s,])"?([a-z][a-z0-9_.]*)"?:\s*"', block))


def test_same_keys_in_both_languages():
    en, de = _keys("en"), _keys("de")
    assert en and en == de, (en ^ de)


def test_every_progression_reason_is_translated():
    src = (ROOT / "progression.py").read_text(encoding="utf-8")
    reasons = set(re.findall(r'"(?:reason_key)":\s*(?:"([a-z_]+)"|[^,]*?"([a-z_]+)" if)', src))
    keys = {k for pair in reasons for k in pair if k} | set(re.findall(r'else "([a-z_]+)"', src))
    assert "hard_hold" in keys and "target_reps" in keys
    en = _keys("en")
    assert not [k for k in keys if f"sug.{k}" not in en]


def test_used_keys_exist():
    en = _keys("en")
    used = set(re.findall(r'\bt\("([a-z0-9_.]+)"', CARD))
    assert not used - en, used - en
