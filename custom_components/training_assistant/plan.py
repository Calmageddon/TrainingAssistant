"""Trainingspläne: einlesen, prüfen und in einzelne Ablauf-Schritte zerlegen.

Bewusst ohne Home-Assistant-Abhängigkeiten, damit tools/validate_plan.py und die
Tests diese Datei direkt nutzen können. Die Prüfung entspricht
schema/plan.schema.json plus Logikregeln, die ein Schema nicht abdecken kann.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

import yaml

# Muskelgruppen für das Feld `muscles` (gleiche Liste wie stats.GROUP_ORDER, siehe tests/test_plan.py).
# Hier als Kopie, damit plan.py auch einzeln (tools/validate_plan.py) läuft.
GROUP_ORDER = ["chest", "back", "shoulders", "biceps", "triceps", "core", "quads", "hamstrings", "glutes", "calves"]

SCHEMA_VERSION = 1

ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
GOALS = {"hypertrophy", "strength", "endurance", "general"}
EQUIPMENT = {"bodyweight", "dumbbell", "kettlebell", "barbell", "band", "machine", "cable", "other"}

BLOCK_FIELDS: dict[str, tuple[set[str], set[str]]] = {
    "warmup": ({"type"}, {"type", "name", "duration_s", "note"}),
    "cooldown": ({"type"}, {"type", "name", "duration_s", "note"}),
    "sets": (
        {"type", "exercise"},
        {"type", "name", "exercise", "sets", "total_reps", "reps", "duration_s", "weight_kg", "per_side", "tempo",
         "rest_s", "rest_after_s", "progression", "note"},
    ),
    "circuit": (
        {"type", "exercises"},
        {"type", "name", "rounds", "time_cap_s", "rest_after_exercise_s", "rest_after_round_s", "rest_after_s",
         "exercises", "tempo", "note"},
    ),
    "interval": (
        {"type", "rounds", "work_s", "rest_s", "exercises"},
        {"type", "name", "rounds", "work_s", "rest_s", "rest_after_s", "exercises", "note"},
    ),
    # Zeitgesteuerte Abfolge mit eigener Dauer je Übung/Haltung (Yoga-Flow, 30-20-10 …)
    "flow": (
        {"type", "exercises"},
        {"type", "name", "rounds", "rest_s", "rest_after_round_s", "rest_after_s", "exercises", "note"},
    ),
}
FLOW_ITEM_FIELDS = {"exercise", "duration_s", "per_side", "note"}

DEFAULT_BLOCK_NAMES = {
    "warmup": "Aufwärmen",
    "cooldown": "Cool Down",
    "sets": "Sätze",
    "circuit": "Zirkel",
    "interval": "HIIT",
    "flow": "Flow",
}

DEFAULT_REST_S = 60
# Obergrenze für offene Blöcke (Zeitlimit / Gesamtwiederholungen ohne feste Anzahl)
OPEN_LIMIT = 50
WEIGHT_STEPS = {"barbell": 2.5, "dumbbell": 2, "kettlebell": 2, "machine": 2.5, "cable": 2.5}
ITEM_FIELDS = {"exercise", "reps", "duration_s", "weight_kg", "per_side", "tempo", "progression", "note"}


# Meldungen stehen auf Deutsch im Code; für Englisch werden sie hier übersetzt.
# Neue Meldung = auch hier ein Muster ergänzen (tests/test_plan.py prüft das).
EN_MESSAGES: list[tuple[str, str]] = [
    (r"^Text ist kein gültiges YAML/JSON: (.*)$", r"Text is not valid YAML/JSON: \1"),
    (r"^muss ein Objekt sein$", "must be an object"),
    (r"^Pflichtfeld '(.+)' fehlt$", r"required field '\1' is missing"),
    (r"^unbekanntes Feld '(.+)'$", r"unknown field '\1'"),
    (r"^muss eine ganze Zahl ≥ (\S+) sein$", r"must be a whole number ≥ \1"),
    (r"^muss eine Zahl sein$", "must be a number"),
    (r"^muss größer als 0 sein$", "must be greater than 0"),
    (r"^darf nicht negativ sein$", "must not be negative"),
    (r"^muss ein nicht-leerer Text sein$", "must be a non-empty text"),
    (r"^'(.*)' ist keine gültige ID .*$", r"'\1' is not a valid ID (lowercase a–z, 0–9, _; starting with a letter)"),
    (r"^min ist größer als max$", "min is greater than max"),
    (r"^type muss double, linear, reps oder none sein$", "type must be double, linear, reps or none"),
    (r"^braucht entweder 'reps' oder 'duration_s'.*$", "needs either 'reps' or 'duration_s' (exactly one of them)"),
    (r"^muss true oder false sein$", "must be true or false"),
    (r'^muss ein Text sein, z\. B\. "3-0-1"$', 'must be a text, e.g. "3-0-1"'),
    (r"^muss (\d+) sein$", r"must be \1"),
    (r"^muss ein Text sein$", "must be a text"),
    (r"^muss eines von (.+) sein$", r"must be one of \1"),
    (r"^muss ein Objekt mit mindestens einer Übung sein$", "must be an object with at least one exercise"),
    (r"^muss eine Bild-ID aus dem Katalog sein.*$", "must be an image ID from the catalog (e.g. Goblet_Squat) or false"),
    (r"^muss eine Liste von Texten sein$", "must be a list of texts"),
    (r"^muss eine Liste von Muskelgruppen sein \((.+)\), \[\] = keiner zuordnen$",
     r"must be a list of muscle groups (\1), [] = assign to none"),
    (r"^muss eine Liste mit mindestens einem Workout sein$", "must be a list with at least one workout"),
    (r"^Workout-ID '(.+)' kommt mehrfach vor$", r"workout ID '\1' is used more than once"),
    (r"^muss eine Liste mit mindestens einem Block sein$", "must be a list with at least one block"),
    (r"^Übung '(.+)' steht nicht im Katalog 'exercises'$", r"exercise '\1' is not in the 'exercises' catalog"),
    (r"^doppelte Progression braucht.*$",
     "double progression needs a rep range (reps: {min, max}) – or use 'progression: {type: linear, …}' "
     "or '{type: none}'"),
    (r"^braucht 'sets'.*$", "needs 'sets' (number of sets) or 'total_reps' (sets until the total is reached)"),
    (r"^'total_reps' passt nicht zu Zeit-Sätzen$", "'total_reps' does not work with timed sets"),
    (r"^braucht 'rounds'.*$", "needs 'rounds' (number of rounds) or 'time_cap_s' (rounds until the time is up)"),
    (r"^muss eine Liste mit mindestens einer Übung sein$", "must be a list with at least one exercise"),
    (r"^muss eine Liste mit mindestens einer Übungs-ID sein$", "must be a list with at least one exercise ID"),
]


def translate_message(msg: str, lang: str | None) -> str:
    """Deutsche Prüfmeldung in die gewünschte Sprache (aktuell en/de)."""
    if (lang or "en").split("-")[0].lower() == "de":
        return msg
    for pattern, repl in EN_MESSAGES:
        if re.match(pattern, msg):
            return re.sub(pattern, repl, msg)
    return msg


class PlanError(ValueError):
    """Plan ist ungültig. `errors` enthält alle Meldungen."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors


# ---------------------------------------------------------------------------
# Einlesen
# ---------------------------------------------------------------------------


def parse_plan_text(text: str, lang: str | None = "en") -> dict[str, Any]:
    """YAML/JSON-Text lesen und prüfen. Wirft PlanError bei Fehlern (Meldungen in `lang`)."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as err:
        raise PlanError([translate_message(f"Text ist kein gültiges YAML/JSON: {err}", lang)]) from err
    errors = validate_plan(data, lang)
    if errors:
        raise PlanError(errors)
    return data


def slugify(text: str) -> str:
    """Einfache ID aus einem Namen (für Plan-IDs)."""
    text = text.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "plan"


# ---------------------------------------------------------------------------
# Prüfung
# ---------------------------------------------------------------------------


class _Checker:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def err(self, path: str, msg: str) -> None:
        self.errors.append(f"{path}: {msg}" if path else msg)

    def obj(self, value: Any, path: str, required: set[str], allowed: set[str]) -> bool:
        if not isinstance(value, dict):
            self.err(path, "muss ein Objekt sein")
            return False
        for key in sorted(required - value.keys()):
            self.err(path, f"Pflichtfeld '{key}' fehlt")
        for key in sorted(value.keys() - allowed):
            self.err(path, f"unbekanntes Feld '{key}'")
        return True

    def integer(self, value: Any, path: str, minimum: int = 0) -> bool:
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            self.err(path, f"muss eine ganze Zahl ≥ {minimum} sein")
            return False
        return True

    def number(self, value: Any, path: str, *, positive: bool = False, nullable: bool = False) -> bool:
        if value is None and nullable:
            return True
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            self.err(path, "muss eine Zahl sein")
            return False
        if value < 0 or (positive and value == 0):
            self.err(path, "muss größer als 0 sein" if positive else "darf nicht negativ sein")
            return False
        return True

    def text(self, value: Any, path: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            self.err(path, "muss ein nicht-leerer Text sein")
            return False
        return True

    def ident(self, value: Any, path: str) -> bool:
        if not isinstance(value, str) or not ID_RE.match(value):
            self.err(path, f"'{value}' ist keine gültige ID (klein, a–z, 0–9, _; beginnt mit Buchstabe)")
            return False
        return True

    def reps(self, value: Any, path: str) -> None:
        if value == "max":
            return
        self.int_or_range(value, path, 1)

    def int_or_range(self, value: Any, path: str, minimum: int) -> None:
        if isinstance(value, dict):
            if self.obj(value, path, {"min", "max"}, {"min", "max"}):
                ok = self.integer(value.get("min"), f"{path}/min", minimum) and self.integer(
                    value.get("max"), f"{path}/max", minimum
                )
                if ok and value["min"] > value["max"]:
                    self.err(path, "min ist größer als max")
        else:
            self.integer(value, path, minimum)

    def progression(self, value: Any, path: str) -> None:
        if not isinstance(value, dict):
            self.err(path, "muss ein Objekt sein")
            return
        ptype = value.get("type")
        if ptype in ("double", "linear"):
            if self.obj(value, path, {"type", "increment_kg"}, {"type", "increment_kg"}):
                if "increment_kg" in value:
                    self.number(value["increment_kg"], f"{path}/increment_kg", positive=True)
        elif ptype == "reps":
            if self.obj(value, path, {"type"}, {"type", "increment", "max_reps"}):
                if "increment" in value:
                    self.integer(value["increment"], f"{path}/increment", 1)
                if "max_reps" in value:
                    self.integer(value["max_reps"], f"{path}/max_reps", 1)
        elif ptype == "none":
            self.obj(value, path, {"type"}, {"type"})
        else:
            self.err(path, "type muss double, linear, reps oder none sein")

    def target(self, item: dict, path: str) -> None:
        has_reps, has_dur = "reps" in item, "duration_s" in item
        if has_reps == has_dur:
            self.err(path, "braucht entweder 'reps' oder 'duration_s' (genau eins von beiden)")
        if has_reps:
            self.reps(item["reps"], f"{path}/reps")
        if has_dur and item["duration_s"] != "max":
            self.int_or_range(item["duration_s"], f"{path}/duration_s", 1)
        if "per_side" in item and not isinstance(item["per_side"], bool):
            self.err(f"{path}/per_side", "muss true oder false sein")
        if "tempo" in item and not isinstance(item["tempo"], str):
            self.err(f"{path}/tempo", "muss ein Text sein, z. B. \"3-0-1\"")


def validate_plan(plan: Any, lang: str | None = "en") -> list[str]:
    """Alle Fehler eines Plans als Liste (Meldungen in `lang`). Leere Liste = gültig."""
    errors = _validate(plan)
    return [_translate_line(e, lang) for e in errors]


def _translate_line(line: str, lang: str | None) -> str:
    path, sep, msg = line.partition(": ")
    if sep and "/" in path or path in ("schema_version", "name", "description", "goal", "defaults", "exercises",
                                      "workouts"):
        return f"{path}: {translate_message(msg, lang)}"
    return translate_message(line, lang)


def _validate(plan: Any) -> list[str]:
    c = _Checker()
    if not c.obj(
        plan,
        "",
        {"schema_version", "name", "exercises", "workouts"},
        {"schema_version", "name", "description", "goal", "defaults", "exercises", "workouts"},
    ):
        return c.errors

    if "schema_version" in plan and plan["schema_version"] != SCHEMA_VERSION:
        c.err("schema_version", f"muss {SCHEMA_VERSION} sein")
    if "name" in plan:
        c.text(plan["name"], "name")
    if "description" in plan and not isinstance(plan["description"], str):
        c.err("description", "muss ein Text sein")
    if "goal" in plan and plan["goal"] not in GOALS:
        c.err("goal", f"muss eines von {', '.join(sorted(GOALS))} sein")

    defaults = plan.get("defaults", {})
    if "defaults" in plan and c.obj(defaults, "defaults", set(), {"rest_s", "progression"}):
        if "rest_s" in defaults:
            c.integer(defaults["rest_s"], "defaults/rest_s")
        if "progression" in defaults:
            c.progression(defaults["progression"], "defaults/progression")

    catalog = plan.get("exercises")
    if "exercises" in plan:
        if not isinstance(catalog, dict) or not catalog:
            c.err("exercises", "muss ein Objekt mit mindestens einer Übung sein")
            catalog = {}
        for ex_id, ex in catalog.items():
            path = f"exercises/{ex_id}"
            c.ident(ex_id, path)
            if c.obj(ex, path, {"name"}, {"name", "aliases", "equipment", "note", "image", "muscles"}):
                if "muscles" in ex and not (
                    isinstance(ex["muscles"], list) and all(m in GROUP_ORDER for m in ex["muscles"])
                ):
                    c.err(f"{path}/muscles",
                          f"muss eine Liste von Muskelgruppen sein ({', '.join(GROUP_ORDER)}), [] = keiner zuordnen")
                if "image" in ex and not (ex["image"] is False or (isinstance(ex["image"], str) and ex["image"])):
                    c.err(f"{path}/image", "muss eine Bild-ID aus dem Katalog sein (z. B. Goblet_Squat) oder false")
                if "name" in ex:
                    c.text(ex["name"], f"{path}/name")
                if "aliases" in ex and not (
                    isinstance(ex["aliases"], list) and all(isinstance(a, str) for a in ex["aliases"])
                ):
                    c.err(f"{path}/aliases", "muss eine Liste von Texten sein")
                if "equipment" in ex and ex["equipment"] not in EQUIPMENT:
                    c.err(f"{path}/equipment", f"muss eines von {', '.join(sorted(EQUIPMENT))} sein")
    catalog = catalog if isinstance(catalog, dict) else {}

    workouts = plan.get("workouts")
    if "workouts" in plan and (not isinstance(workouts, list) or not workouts):
        c.err("workouts", "muss eine Liste mit mindestens einem Workout sein")
        workouts = []
    seen: set[str] = set()
    for wi, w in enumerate(workouts or []):
        wpath = f"workouts/{wi}"
        if not c.obj(w, wpath, {"id", "name", "blocks"}, {"id", "name", "note", "blocks"}):
            continue
        if "id" in w and c.ident(w["id"], f"{wpath}/id"):
            if w["id"] in seen:
                c.err(f"{wpath}/id", f"Workout-ID '{w['id']}' kommt mehrfach vor")
            seen.add(w["id"])
        if "name" in w:
            c.text(w["name"], f"{wpath}/name")
        blocks = w.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            c.err(f"{wpath}/blocks", "muss eine Liste mit mindestens einem Block sein")
            continue
        for bi, block in enumerate(blocks):
            _check_block(c, block, f"{wpath}/blocks/{bi}", catalog, defaults if isinstance(defaults, dict) else {})
    return c.errors


def _check_block(c: _Checker, block: Any, path: str, catalog: dict, defaults: dict) -> None:
    if not isinstance(block, dict):
        c.err(path, "muss ein Objekt sein")
        return
    btype = block.get("type")
    if btype not in BLOCK_FIELDS:
        c.err(f"{path}/type", f"muss eines von {', '.join(BLOCK_FIELDS)} sein")
        return
    required, allowed = BLOCK_FIELDS[btype]
    if not c.obj(block, path, required, allowed):
        return
    if "name" in block:
        c.text(block["name"], f"{path}/name")
    for key in ("duration_s", "rest_s", "rest_after_exercise_s", "rest_after_round_s", "rest_after_s",
                "time_cap_s", "total_reps"):
        if key in block and not (btype == "sets" and key == "duration_s"):
            c.integer(block[key], f"{path}/{key}")

    def check_exercise_ref(ex: Any, p: str) -> None:
        if c.ident(ex, p) and ex not in catalog:
            c.err(p, f"Übung '{ex}' steht nicht im Katalog 'exercises'")

    def check_item(item: dict, p: str) -> None:
        if "exercise" in item:
            check_exercise_ref(item["exercise"], f"{p}/exercise")
        c.target(item, p)
        if "weight_kg" in item:
            c.number(item["weight_kg"], f"{p}/weight_kg", nullable=True)
        if "progression" in item:
            c.progression(item["progression"], f"{p}/progression")
        # Zeit-Sätze und reps: max werden ohne Progression geführt; feste reps brauchen für
        # „double“ einen Bereich.
        prog = item.get("progression") or defaults.get("progression")
        if isinstance(prog, dict) and prog.get("type") == "double" and isinstance(item.get("reps"), int) \
                and not isinstance(item.get("reps"), bool):
            c.err(p, "doppelte Progression braucht einen Wiederholungsbereich (reps: {min, max}) – "
                     "oder setze 'progression: {type: linear, …}' bzw. '{type: none}'")

    if btype == "sets":
        if "sets" in block:
            c.integer(block["sets"], f"{path}/sets", 1)
        elif "total_reps" not in block:
            c.err(path, "braucht 'sets' (Anzahl Sätze) oder 'total_reps' (Sätze bis zur Gesamtzahl)")
        if "total_reps" in block and "duration_s" in block:
            c.err(path, "'total_reps' passt nicht zu Zeit-Sätzen")
        check_item(block, path)
    elif btype == "circuit":
        if "rounds" in block:
            c.integer(block["rounds"], f"{path}/rounds", 1)
        elif "time_cap_s" not in block:
            c.err(path, "braucht 'rounds' (Anzahl Runden) oder 'time_cap_s' (Runden bis die Zeit um ist)")
        if "tempo" in block and not isinstance(block["tempo"], str):
            c.err(f"{path}/tempo", "muss ein Text sein")
        items = block.get("exercises")
        if not isinstance(items, list) or not items:
            c.err(f"{path}/exercises", "muss eine Liste mit mindestens einer Übung sein")
            return
        for ii, item in enumerate(items):
            ipath = f"{path}/exercises/{ii}"
            if c.obj(item, ipath, {"exercise"}, ITEM_FIELDS):
                check_item(item, ipath)
    elif btype == "flow":
        if "rounds" in block:
            c.integer(block["rounds"], f"{path}/rounds", 1)
        items = block.get("exercises")
        if not isinstance(items, list) or not items:
            c.err(f"{path}/exercises", "muss eine Liste mit mindestens einer Übung sein")
            return
        for ii, item in enumerate(items):
            ipath = f"{path}/exercises/{ii}"
            if c.obj(item, ipath, {"exercise", "duration_s"}, FLOW_ITEM_FIELDS):
                check_exercise_ref(item["exercise"], f"{ipath}/exercise")
                c.integer(item["duration_s"], f"{ipath}/duration_s", 1)
                if "per_side" in item and not isinstance(item["per_side"], bool):
                    c.err(f"{ipath}/per_side", "muss true oder false sein")
    elif btype == "interval":
        c.integer(block.get("rounds"), f"{path}/rounds", 1)
        c.integer(block.get("work_s"), f"{path}/work_s", 1)
        items = block.get("exercises")
        if not isinstance(items, list) or not items:
            c.err(f"{path}/exercises", "muss eine Liste mit mindestens einer Übungs-ID sein")
            return
        for ii, ex in enumerate(items):
            check_exercise_ref(ex, f"{path}/exercises/{ii}")


# ---------------------------------------------------------------------------
# Ablauf-Schritte
# ---------------------------------------------------------------------------


def rep_bounds(reps: Any) -> tuple[int, int] | None:
    """(min, max) eines reps-Werts. None bei Zeit-Sätzen und bei reps: max."""
    if isinstance(reps, dict):
        return reps["min"], reps["max"]
    if isinstance(reps, int) and not isinstance(reps, bool):
        return reps, reps
    return None


def duration_bounds(duration: Any) -> tuple[int, int] | None:
    if isinstance(duration, dict):
        return duration["min"], duration["max"]
    if isinstance(duration, int) and not isinstance(duration, bool):
        return duration, duration
    return None


def find_workout(plan: dict, workout_id: str) -> dict:
    for w in plan["workouts"]:
        if w["id"] == workout_id:
            return w
    raise KeyError(workout_id)


HistoryLookup = Callable[[str], list[dict]]


def flow_segments(block: dict, catalog: dict) -> list[dict[str, Any]]:
    """Abfolge eines Flow-Blocks in einzelne Zeitabschnitte zerlegen.

    Pro Runde jede Übung (bei per_side links und rechts), danach rest_s Übergang;
    nach jeder Runde (außer der letzten) rest_after_round_s statt rest_s. Der letzte Abschnitt hat keine Pause.
    """
    rounds = block.get("rounds", 1)
    rest = block.get("rest_s", 0)
    round_rest = block.get("rest_after_round_s", rest)
    segs: list[dict[str, Any]] = []
    for r in range(1, rounds + 1):
        for item in block["exercises"]:
            ex = catalog[item["exercise"]]
            for side in (("left", "right") if item.get("per_side") else (None,)):
                segs.append({"exercise": item["exercise"], "name": ex["name"], "side": side, "round": r,
                             "work_s": item["duration_s"], "rest_s": rest, "note": item.get("note")})
        if segs:
            segs[-1]["rest_s"] = round_rest
    if segs:
        segs[-1]["rest_s"] = 0
    return segs


def interval_segments(block: dict, catalog: dict) -> list[dict[str, Any]]:
    """Klassischer HIIT-Block (gleiche Arbeits-/Pausenzeit, Übungen reihum) als Zeitabschnitte."""
    ids = block["exercises"]
    rounds = block["rounds"]
    return [
        {"exercise": ids[(r - 1) % len(ids)], "name": catalog[ids[(r - 1) % len(ids)]]["name"], "side": None,
         "round": r, "work_s": block["work_s"], "rest_s": block["rest_s"] if r < rounds else 0, "note": None}
        for r in range(1, rounds + 1)
    ]


def flow_step(block: dict, bi: int, name: str | None, catalog: dict) -> dict[str, Any]:
    segs = flow_segments(block, catalog)
    return {
        "type": "interval",  # läuft wie HIIT zeitgesteuert, aber mit eigener Dauer je Abschnitt
        "block": bi,
        "block_type": "flow",
        "block_name": name,
        "rounds": block.get("rounds", 1),
        "segments": segs,
        "total_s": sum(x["work_s"] + x["rest_s"] for x in segs),
        "exercises": [x["exercise"] for x in block["exercises"]],
        "exercise_names": [catalog[x["exercise"]]["name"] for x in block["exercises"]],
        "items": [{"exercise": x["exercise"], "name": catalog[x["exercise"]]["name"], "duration_s": x["duration_s"],
                   "per_side": bool(x.get("per_side"))} for x in block["exercises"]],
        "note": block.get("note"),
    }


def build_steps(plan: dict, workout_id: str, history: HistoryLookup | None = None) -> list[dict]:
    """Zerlegt ein Workout in eine flache Liste von Schritten.

    `history(exercise_id)` liefert die Sätze der letzten Session mit dieser Übung.
    Daraus werden Zielgewicht und Ziel-Wiederholungen vorgeschlagen.

    Offene Blöcke (Zirkel mit `time_cap_s`, Sätze mit `total_reps`) werden bis
    OPEN_LIMIT ausgerollt; die Engine springt zum nächsten Block, sobald die Zeit um
    bzw. die Gesamtzahl erreicht ist (`block_end` im Schritt).
    """
    from .progression import suggest  # noqa: PLC0415 – lazy, damit Prüfung ohne Paket läuft

    defaults = plan.get("defaults", {})
    def_rest = defaults.get("rest_s", DEFAULT_REST_S)
    def_prog = defaults.get("progression", {"type": "none"})
    catalog = plan["exercises"]
    workout = find_workout(plan, workout_id)
    steps: list[dict] = []

    def set_step(item: dict, block_idx: int, block: dict, **extra: Any) -> dict:
        ex_id = item["exercise"]
        reps = item.get("reps")
        amrap = reps == "max"
        bounds = rep_bounds(reps)
        dur = duration_bounds(item.get("duration_s"))
        progression = item.get("progression") or def_prog
        if bounds is None:
            progression = {"type": "none"}
        plan_weight = item.get("weight_kg")
        last = history(ex_id) if history else []
        sug = suggest(
            last,
            rep_range=bounds,
            progression=progression,
            plan_weight=plan_weight,
        )
        return {
            "type": "set",
            "block": block_idx,
            "block_type": block["type"],
            "block_name": block.get("name"),  # ohne Namen: Anzeige/Ansage übersetzt den Typ
            "exercise": ex_id,
            "exercise_name": catalog[ex_id]["name"],
            "rep_range": list(bounds) if bounds else None,
            "amrap": amrap,
            "target_reps": sug["reps"],
            "target_weight": sug["weight_kg"],
            "target_duration": dur[0] if dur else None,
            "duration_range": list(dur) if dur and dur[0] != dur[1] else None,
            "hold_max": item.get("duration_s") == "max",
            "per_side": bool(item.get("per_side")),
            # Schrittweite für die Plus/Minus-Tasten der Karte
            "weight_step": progression.get("increment_kg") or WEIGHT_STEPS.get(catalog[ex_id].get("equipment"), 1),
            # bester Wert der letzten Session (Startwert bei reps/duration: max)
            "last_reps": max((x["reps"] for x in last if isinstance(x.get("reps"), (int, float))), default=None),
            "tempo": item.get("tempo") or block.get("tempo"),
            "suggestion": sug["reason"],
            "suggestion_key": sug.get("reason_key"),
            "suggestion_params": sug.get("reason_params", {}),
            "progression": progression.get("type", "none"),
            "note": item.get("note") or catalog[ex_id].get("note"),
            **extra,
        }

    for bi, block in enumerate(workout["blocks"]):
        btype = block["type"]
        name = block.get("name")
        if btype in ("warmup", "cooldown"):
            steps.append(
                {
                    "type": btype,
                    "block": bi,
                    "block_type": btype,
                    "block_name": name,
                    "duration_s": block.get("duration_s"),
                    "note": block.get("note"),
                }
            )
        elif btype == "sets":
            fixed = block.get("sets")
            n = fixed or OPEN_LIMIT
            block_end = {"total_reps": block["total_reps"]} if "total_reps" in block else None
            for s in range(1, n + 1):
                steps.append(
                    set_step(block, bi, block, set_no=s, sets=fixed, round=None, rounds=None,
                             rest_after_s=block.get("rest_s", def_rest), block_end=block_end,
                             block_note=block.get("note") if s == 1 else None)
                )
        elif btype == "circuit":
            items = block["exercises"]
            fixed = block.get("rounds")
            rounds = fixed or OPEN_LIMIT
            block_end = {"time_cap_s": block["time_cap_s"]} if "time_cap_s" in block else None
            for r in range(1, rounds + 1):
                for i, item in enumerate(items):
                    last = i == len(items) - 1
                    if not last:
                        rest = block.get("rest_after_exercise_s", 0)
                    elif r < rounds:
                        rest = block.get("rest_after_round_s", 0 if block_end else def_rest)
                    else:
                        rest = 0
                    steps.append(
                        set_step(item, bi, block, set_no=r, sets=fixed, round=r, rounds=fixed,
                                 rest_after_s=rest, block_end=block_end,
                                 block_note=block.get("note") if r == 1 and i == 0 else None)
                    )
        elif btype == "flow":
            steps.append(flow_step(block, bi, name, catalog))
        elif btype == "interval":
            steps.append(
                {
                    "type": "interval",
                    "block": bi,
                    "block_type": btype,
                    "block_name": name,
                    "rounds": block["rounds"],
                    "work_s": block["work_s"],
                    "rest_s": block["rest_s"],
                    "exercises": block["exercises"],
                    "exercise_names": [catalog[e]["name"] for e in block["exercises"]],
                    "segments": interval_segments(block, catalog),
                    "note": block.get("note"),
                }
            )

        block_rest = block.get("rest_after_s")
        block_steps = [x for x in steps if x["block"] == bi]
        for x in block_steps:
            x["block_rest_s"] = block_rest or 0
        if block_rest is not None and block_steps and block_steps[-1]["type"] == "set":
            block_steps[-1]["rest_after_s"] = block_rest

    for i, step in enumerate(steps):
        step["idx"] = i
    return steps
