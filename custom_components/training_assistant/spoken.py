"""Gesprochene Antworten verstehen – Deutsch und Englisch.

„acht mal fünfzehn“, „zwölfeinhalb Kilo“, „ja“ / „eight times fifteen“,
„twelve and a half kilos“, „yes“. Ohne Home-Assistant-Abhängigkeiten.

Neue Sprache: LANGS um einen Eintrag ergänzen (Zahlwörter, Einheiten, Ja-/Überspringen-Wörter).
"""

from __future__ import annotations

import re
from typing import Any

LANGS: dict[str, dict[str, Any]] = {
    "de": {
        "units": {
            "null": 0, "eins": 1, "zwei": 2, "zwo": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6,
            "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11, "zwölf": 12, "dreizehn": 13,
            "vierzehn": 14, "fünfzehn": 15, "sechzehn": 16, "siebzehn": 17, "achtzehn": 18, "neunzehn": 19,
        },
        "compound_units": {"ein": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6,
                           "sieben": 7, "acht": 8, "neun": 9},
        "tens": {"zwanzig": 20, "dreißig": 30, "dreissig": 30, "vierzig": 40, "fünfzig": 50,
                 "sechzig": 60, "siebzig": 70, "achtzig": 80, "neunzig": 90},
        "hundred": "hundert",
        "and": "und",
        "half_suffix": "einhalb",
        "one_and_half": {"anderthalb", "eineinhalb"},
        "half_words": {"einhalb", "halb"},
        "point": {"komma"},
        "articles": {"ein", "eine", "einen"},
        "kg": {"kilo", "kilos", "kg", "kilogramm"},
        "reps": {"wiederholungen", "wiederholung", "wdh", "reps", "rep", "stück", "mal", "x"},
        "seconds": {"sekunden", "sekunde", "sek", "s"},
        "confirm": {"ja", "jo", "jap", "jawohl", "genau", "passt", "richtig", "korrekt", "stimmt", "ok", "okay",
                    "geplant", "yes", "jep", "klar", "sicher"},
        "skip": {"übersprungen", "ausgelassen", "skip", "überspringen", "auslassen"},
        "easy": {"leicht", "locker", "einfach", "easy", "lässig", "entspannt"},
        "hard": {"schwer", "hart", "anstrengend", "brutal", "knapp", "heftig", "zäh"},
    },
    "en": {
        "units": {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
            "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
        },
        "compound_units": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                           "eight": 8, "nine": 9},
        "tens": {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
                 "eighty": 80, "ninety": 90},
        "hundred": "hundred",
        "and": "and",
        "half_suffix": None,
        "one_and_half": set(),
        "half_words": {"half"},
        "point": {"point", "dot"},
        "articles": {"a", "an"},
        "kg": {"kilo", "kilos", "kg", "kgs", "kilogram", "kilograms"},
        "reps": {"reps", "rep", "repetitions", "repetition", "times", "x"},
        "seconds": {"seconds", "second", "secs", "sec", "s"},
        "confirm": {"yes", "yeah", "yep", "yup", "correct", "right", "planned", "ok", "okay", "sure", "done",
                    "affirmative"},
        "skip": {"skipped", "skip", "skipping"},
        "easy": {"easy", "light", "comfortable", "effortless"},
        "hard": {"hard", "tough", "heavy", "difficult", "brutal", "grinding", "struggled"},
    },
}

_TOKEN_RE = re.compile(r"\d+(?:[.,]\d+)?|[a-zäöüß]+")


def _lang(lang: str | None) -> dict[str, Any]:
    base = (lang or "de").split("-")[0].lower()
    return LANGS.get(base, LANGS["en"])


def _int_word(word: str, L: dict[str, Any]) -> int | None:
    if not word:
        return None
    if word in L["units"]:
        return L["units"][word]
    if word in L["tens"]:
        return L["tens"][word]
    hundred = L["hundred"]
    if hundred in word:
        left, _, right = word.partition(hundred)
        lval = 1 if left in ("", "ein", "eins", "one", "a") else _int_word(left, L)
        rval = 0 if right == "" else _int_word(right.removeprefix(L["and"]), L)
        if lval is None or rval is None:
            return None
        return lval * 100 + rval
    if L["and"] in word:  # deutsch: „zweiundzwanzig“
        left, _, right = word.partition(L["and"])
        if left in L["compound_units"] and right in L["tens"]:
            return L["compound_units"][left] + L["tens"][right]
    return None


def word_to_number(word: str, lang: str | None = "de") -> float | None:
    """Ein Wort als Zahl: „acht“ → 8, „zwölfeinhalb“ → 12.5, „twelve“ → 12."""
    L = _lang(lang)
    word = word.lower()
    if word in L["one_and_half"]:
        return 1.5
    suffix = L["half_suffix"]
    if suffix and word.endswith(suffix) and word != suffix:
        base = _int_word(word[: -len(suffix)], L)
        return None if base is None else base + 0.5
    value = _int_word(word, L)
    return None if value is None else float(value)


def extract_numbers(text: str, lang: str | None = "de") -> list[tuple[float, str | None]]:
    """Zahlen im Text mit der Einheit dahinter: [(8, 'reps'), (15, 'kg')]."""
    L = _lang(lang)
    tokens = _TOKEN_RE.findall(text.lower().replace("-", " "))
    result: list[list[Any]] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok[0].isdigit():
            value: float | None = float(tok.replace(",", "."))
        elif tok in L["articles"]:
            value = None  # „ein bisschen“, „a bit“ – keine Zahl
        else:
            value = word_to_number(tok, lang)
        if value is None:
            if result and result[-1][1] is None:
                if tok in L["kg"]:
                    result[-1][1] = "kg"
                elif tok in L["reps"]:
                    result[-1][1] = "reps"
                elif tok in L["seconds"]:
                    result[-1][1] = "s"
            i += 1
            continue
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        # englisch: „twenty five“ / „twenty-five“
        if value in L["tens"].values() and nxt in L["compound_units"]:
            value += L["compound_units"][nxt]
            i += 1
            nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        # „zwölf komma fünf“ / „twelve point five“
        if nxt in L["point"] and i + 2 < len(tokens):
            frac_tok = tokens[i + 2]
            frac_val = frac_tok if frac_tok.isdigit() else word_to_number(frac_tok, lang)
            if frac_val is not None:
                value = float(f"{int(value)}.{frac_tok if frac_tok.isdigit() else int(frac_val)}")
                i += 2
        # „zwölf einhalb“ / „twelve and a half“ / „twelve half“
        elif nxt in L["half_words"]:
            value += 0.5
            i += 1
        elif nxt == L["and"] and i + 3 < len(tokens) and tokens[i + 2] in L["articles"] \
                and tokens[i + 3] in L["half_words"]:
            value += 0.5
            i += 3
        result.append([value, None])
        i += 1
    return [(v, u) for v, u in result]


def parse_answer(text: str | None, *, timed: bool = False, lang: str | None = "de") -> dict[str, Any]:
    """Antwort auf „8 mal 15 Kilo wie geplant?“ / „8 reps with 15 kilos as planned?“ auswerten.

    Rückgabe: {"kind": "confirm"|"correct"|"skip"|"unknown", "reps", "weight_kg", "duration_s", "effort"}
    effort: "easy" / "hard" / None – „ja, war locker“, „acht, war schwer“, „yes, easy“.
    """
    L = _lang(lang)
    out: dict[str, Any] = {"kind": "unknown", "reps": None, "weight_kg": None, "duration_s": None, "effort": None}
    if not text or not text.strip():
        return out
    words = set(_TOKEN_RE.findall(text.lower()))
    if words & L["skip"]:
        out["kind"] = "skip"
        return out
    if words & L["hard"]:
        out["effort"] = "hard"
    elif words & L["easy"]:
        out["effort"] = "easy"

    numbers = extract_numbers(text, lang)
    if not numbers:
        if words & L["confirm"] or out["effort"]:
            out["kind"] = "confirm"
        return out

    free: list[float] = []
    for value, unit in numbers:
        if unit == "kg" and out["weight_kg"] is None:
            out["weight_kg"] = value
        elif unit == "s" and out["duration_s"] is None:
            out["duration_s"] = int(value)
        elif unit == "reps" and out["reps"] is None:
            out["reps"] = int(value)
        else:
            free.append(value)
    # Zahlen ohne Einheit: zuerst Wiederholungen (bzw. Sekunden), dann Gewicht
    for value in free:
        if timed and out["duration_s"] is None:
            out["duration_s"] = int(value)
        elif not timed and out["reps"] is None and value == int(value):
            out["reps"] = int(value)
        elif out["weight_kg"] is None:
            out["weight_kg"] = value
    if out["reps"] is None and out["weight_kg"] is None and out["duration_s"] is None:
        return out
    out["kind"] = "correct"
    return out
