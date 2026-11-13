import copy
from pathlib import Path

import pytest
import yaml

from custom_components.training_assistant.plan import PlanError, build_steps, parse_plan_text, validate_plan

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize("name", sorted(p.name for p in EXAMPLES.glob("*.yaml")))
def test_examples_valid(name):
    plan = parse_plan_text((EXAMPLES / name).read_text())
    for w in plan["workouts"]:
        assert build_steps(plan, w["id"])


def load(name="ganzkoerper.yaml"):
    return yaml.safe_load((EXAMPLES / name).read_text())


@pytest.mark.parametrize(
    ("mutate", "fragment"),
    [
        (lambda p: p["workouts"][0]["blocks"][1]["exercises"][0].update(exercise="bench"), "nicht im Katalog"),
        (lambda p: p["workouts"][1]["blocks"][2].update(reps=10), "Wiederholungsbereich"),
        (lambda p: p["workouts"][1]["blocks"][3].update(reps=10), "genau eins"),
        (lambda p: p["workouts"][0]["blocks"][0].update(type="stretching"), "type"),
        (lambda p: p["workouts"][0]["blocks"][1]["exercises"][1].update(reps={"min": 12, "max": 8}), "min ist größer"),
        (lambda p: p.update(schema_version=2), "schema_version"),
        (lambda p: p["workouts"][0]["blocks"][1].pop("rounds"), "time_cap_s"),
        (lambda p: p["workouts"][1]["blocks"][1].pop("sets"), "total_reps"),
        (lambda p: p["workouts"][0]["blocks"][1].update(foo=1), "unbekanntes Feld"),
        (lambda p: p["defaults"].update(progression={"type": "reps", "increment": 0}), "increment"),
        (lambda p: p["defaults"].update(progression={"type": "reps", "step": 1}), "unbekanntes Feld 'step'"),
        (lambda p: p["defaults"].update(progression={"type": "wave"}), "double, linear, reps oder none"),
        (lambda p: p["exercises"]["plank"].update(image=3), "Bild-ID"),
    ],
)
def test_invalid(mutate, fragment):
    plan = copy.deepcopy(load())
    mutate(plan)
    errors = validate_plan(plan, "de")
    assert any(fragment in e for e in errors), errors
    english = validate_plan(plan, "en")
    assert len(english) == len(errors)
    german_words = ("muss", "Übung", "Pflicht", "unbekannt", "braucht", "größer", "Liste", "kommt")
    assert not [e for e in english if any(w in e.split(": ", 1)[-1] for w in german_words)], english


def test_parse_error_is_plan_error():
    with pytest.raises(PlanError):
        parse_plan_text("name: [unclosed")


def test_build_steps_circuit():
    plan = load()
    steps = build_steps(plan, "a")
    sets = [s for s in steps if s["type"] == "set"]
    assert len(sets) == 3 * 4  # 3 Runden × 4 Übungen
    assert sets[0]["exercise_name"] == "Push-Ups" and sets[0]["round"] == 1
    assert sets[3]["rest_after_s"] == 120  # Rundenpause
    assert sets[-1]["rest_after_s"] == 0
    assert steps[-1]["type"] == "cooldown"
    assert [s["idx"] for s in steps] == list(range(len(steps)))


def test_build_steps_uses_history():
    plan = load()
    hist = {"goblet_squat": [{"reps": 12, "weight_kg": 16, "status": "confirmed"}] * 3}
    steps = build_steps(plan, "a", lambda ex: hist.get(ex, []))
    goblet = next(s for s in steps if s.get("exercise") == "goblet_squat")
    assert goblet["target_weight"] == 18.5 and goblet["target_reps"] == 8


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_fixture():
    return yaml.safe_load((FIXTURES / "feature-testplan.yaml").read_text())


def test_fixture_valid():
    plan = parse_plan_text((FIXTURES / "feature-testplan.yaml").read_text())
    for w in plan["workouts"]:
        assert build_steps(plan, w["id"])


def test_feature_plan():
    plan = load_fixture()
    w3 = build_steps(plan, "w3")
    plank = next(s for s in w3 if s.get("exercise") == "plank")
    assert plank["hold_max"] and plank["target_duration"] is None
    w4 = build_steps(plan, "w4")
    pull = [s for s in w4 if s.get("exercise") == "pull_up"]
    assert pull[0]["block_end"] == {"total_reps": 20} and pull[0]["amrap"]
    w1 = build_steps(plan, "w1")
    row = next(s for s in w1 if s.get("exercise") == "single_arm_db_row")
    assert row["per_side"]
    last_a = [s for s in w1 if s.get("block_name") == "Zirkel A"][-1]
    assert last_a["rest_after_s"] == 120  # Blockpause


def test_weight_step_and_last_reps():
    plan = load_fixture()
    steps = build_steps(plan, "w3", lambda ex: [{"reps": 7, "status": "confirmed"}] if ex == "chin_up" else [])
    dl = next(s for s in steps if s.get("exercise") == "bb_deadlift")
    assert dl["weight_step"] == 2  # increment_kg aus defaults.progression
    plan["defaults"]["progression"] = {"type": "none"}
    steps = build_steps(plan, "w3", lambda ex: [{"reps": 7, "status": "confirmed"}] if ex == "chin_up" else [])
    assert next(s for s in steps if s.get("exercise") == "bb_deadlift")["weight_step"] == 2.5  # Langhantel
    assert next(s for s in steps if s.get("exercise") == "chin_up")["last_reps"] == 7


def test_every_german_message_has_english_pattern():
    """Jede Meldung im Code (c.err/self.err mit Textliteral) muss ein englisches Muster haben."""
    import re as _re

    from custom_components.training_assistant.plan import EN_MESSAGES

    source = (Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant" / "plan.py").read_text()
    literals = _re.findall(r'(?:self|c)\.err\([^,]+,\s*f?"((?:[^"\\]|\\.)+)"', source)
    assert literals
    for lit in literals:
        sample = _re.sub(r"\{[^}]*\}", "1", lit.replace('\\"', '"'))
        assert any(_re.match(p, sample) for p, _ in EN_MESSAGES), lit


def test_muscles_field():
    from custom_components.training_assistant import plan as plan_mod, stats

    assert plan_mod.GROUP_ORDER == stats.GROUP_ORDER
    plan = copy.deepcopy(load())
    plan["exercises"]["plank"]["muscles"] = ["core"]
    plan["exercises"]["goblet_squat"]["muscles"] = []
    assert validate_plan(plan, "de") == []
    plan["exercises"]["plank"]["muscles"] = ["abs"]
    errors = validate_plan(plan, "en")
    assert errors and "muscle groups" in errors[0]


def test_flow_block():
    plan = {
        "schema_version": 1, "name": "Flow", "exercises": {
            "dog": {"name": "Downward Dog", "image": False}, "warrior": {"name": "Warrior II", "image": False}},
        "workouts": [{"id": "w", "name": "W", "blocks": [
            {"type": "flow", "name": "Sun", "rounds": 2, "rest_s": 5, "rest_after_round_s": 20, "exercises": [
                {"exercise": "dog", "duration_s": 30}, {"exercise": "warrior", "duration_s": 40, "per_side": True}]},
            {"type": "cooldown"}]}],
    }
    assert validate_plan(plan, "de") == []
    step = build_steps(plan, "w")[0]
    assert step["type"] == "interval" and step["block_type"] == "flow"
    segs = step["segments"]
    assert [(s["exercise"], s["side"], s["work_s"], s["rest_s"]) for s in segs] == [
        ("dog", None, 30, 5), ("warrior", "left", 40, 5), ("warrior", "right", 40, 20),
        ("dog", None, 30, 5), ("warrior", "left", 40, 5), ("warrior", "right", 40, 0)]
    assert step["total_s"] == 2 * (30 + 40 + 40) + 5 + 5 + 20 + 5 + 5
    bad = copy.deepcopy(plan)
    bad["workouts"][0]["blocks"][0]["exercises"][0]["duration_s"] = 0
    bad["workouts"][0]["blocks"][0]["exercises"][1]["reps"] = 5
    errors = validate_plan(bad, "en")
    assert any("duration_s" in e for e in errors) and any("reps" in e for e in errors)


def test_interval_has_segments():
    plan = load()
    hiit = next(s for w in plan["workouts"] for s in build_steps(plan, w["id"]) if s["type"] == "interval")
    assert len(hiit["segments"]) == hiit["rounds"] and hiit["segments"][-1]["rest_s"] == 0


def _sides_plan():
    return {
        "schema_version": 1, "name": "Seiten",
        "exercises": {
            "side_plank": {"name": "Side Plank", "equipment": "bodyweight", "unilateral": True},
            "plank": {"name": "Plank", "equipment": "bodyweight"},
            "lunge": {"name": "Lunge", "equipment": "bodyweight", "unilateral": True},
        },
        "workouts": [{"id": "a", "name": "A", "blocks": [
            {"type": "sets", "exercise": "side_plank", "sets": 2, "duration_s": {"min": 20, "max": 45}},
            {"type": "sets", "exercise": "lunge", "sets": 1, "reps": 10, "per_side": False},
            {"type": "sets", "exercise": "plank", "sets": 1, "duration_s": 30, "progression": {"type": "none"}},
            {"type": "flow", "exercises": [{"exercise": "side_plank", "duration_s": 20}]},
        ]}],
    }


def test_unilateral_field_and_per_side_default():
    from custom_components.training_assistant.plan import SIDE_SWITCH_S
    plan = _sides_plan()
    assert validate_plan(plan) == []
    bad = copy.deepcopy(plan)
    bad["exercises"]["plank"]["unilateral"] = "ja"
    assert any("unilateral" in e for e in validate_plan(bad))
    steps = build_steps(plan, "a")
    side, lunge, plank, flow = steps[0], steps[2], steps[3], steps[4]
    assert side["per_side"] is True and side["side_switch_s"] == SIDE_SWITCH_S
    assert lunge["per_side"] is False  # per_side am Eintrag gilt vor unilateral
    assert plank["per_side"] is False and plank["side_switch_s"] == 0
    assert [x["side"] for x in flow["segments"]] == ["left", "right"]


def test_timed_progression_in_steps():
    plan = _sides_plan()
    last = [{"set_no": 1, "duration_s": 45, "target_duration": 45, "status": "confirmed"}]
    steps = build_steps(plan, "a", lambda ex: last)
    assert steps[0]["target_duration"] == 50 and steps[0]["suggestion_key"] == "time_add"  # über das Ende des Bereichs
    assert steps[3]["target_duration"] == 30 and steps[3]["suggestion_key"] == "fixed"  # progression none am Eintrag
    assert steps[0]["last_duration"] == 45
