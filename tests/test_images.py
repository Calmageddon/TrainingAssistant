from pathlib import Path

import pytest
import yaml

from custom_components.training_assistant.images import COMMON, Catalog, map_plan, norm

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
CAT = Catalog.load()


def test_catalog_loaded():
    assert len(CAT.by_id) > 800
    assert CAT.image_count("Goblet_Squat") == 2


def test_common_ids_exist():
    assert [k for k, v in COMMON.items() if v not in CAT.by_id] == []


@pytest.mark.parametrize(
    ("names", "expected"),
    [
        (["Push-Ups"], "Pushups"),
        (["Chin-ups"], "Chin-Up"),
        (["Goblet Squats"], "Goblet_Squat"),
        (["Barbell Romanian Deadlift"], "Romanian_Deadlift"),
        (["Single-Arm Dumbbell Row"], "One-Arm_Dumbbell_Row"),
        (["Klimmzüge"], "Pullups"),
        (["Rumänisches Kreuzheben"], "Romanian_Deadlift"),
        (["Schulterdrücken"], "Dumbbell_Shoulder_Press"),
        (["Liegestütze"], "Pushups"),
        (["Irgendwas", "Plank"], "Plank"),  # Alias greift
        (["Burpees"], None),  # nicht im Katalog → lieber kein Bild
        (["Incline Cable Something"], None),  # keine unscharfe Zuordnung
    ],
)
def test_match(names, expected):
    assert CAT.match(names) == expected


def test_norm():
    assert norm("Push-Ups") == norm("Pushups") == norm("push ups")
    assert norm("Barbell Front Squat", strip_equipment=True) == "frontsquat"


def test_map_plan_explicit_and_false():
    plan = {"exercises": {
        "a": {"name": "Javelin Press", "image": "Dumbbell_Shoulder_Press"},
        "b": {"name": "Plank", "image": False},
        "c": {"name": "Gibt es nicht", "image": "Quatsch_ID"},
        "goblet_squat": {"name": "Becherkniebeuge"},  # über die Übungs-ID
    }}
    assert map_plan(plan, CAT) == {"a": "Dumbbell_Shoulder_Press", "b": None, "c": None, "goblet_squat": "Goblet_Squat"}


def test_examples_coverage():
    fixtures = EXAMPLES.parent / "tests" / "fixtures"
    for path, minimum in ((EXAMPLES / "ganzkoerper.yaml", 8), (fixtures / "feature-testplan.yaml", 9)):
        mapping = map_plan(yaml.safe_load(path.read_text()), CAT)
        assert sum(1 for v in mapping.values() if v) >= minimum
