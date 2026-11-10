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


# -- Übungsbilder (Piktogramme) ------------------------------------------------

from custom_components.training_assistant.images import FIGURES, Pictos, map_pictos  # noqa: E402

PICTOS = Pictos.load()
PICTO_DIR = Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant" / "pictos"
TEMPLATES = Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant" / "templates"


def test_picto_files_complete():
    """Jedes Bild gibt es in beiden Figuren mit der angegebenen Anzahl Dateien, und nichts darüber hinaus."""
    for fig in FIGURES:
        folders = {p.name for p in (PICTO_DIR / fig).iterdir() if p.is_dir()}
        assert folders == set(PICTOS.images)
        for bild, count in PICTOS.images.items():
            files = sorted(p.name for p in (PICTO_DIR / fig / bild).glob("*.jpg"))
            assert files == [f"{n}.jpg" for n in range(count)], (fig, bild)


@pytest.mark.parametrize("path", sorted(TEMPLATES.glob("*.yaml")), ids=lambda p: p.stem)
def test_every_template_exercise_has_picto(path):
    plan = yaml.safe_load(path.read_text(encoding="utf-8"))
    pictos = map_pictos(plan, PICTOS, map_plan(plan, CAT))
    assert [k for k, v in pictos.items() if not v] == []


@pytest.mark.parametrize(
    ("ex_id", "ex", "catalog_id", "expected"),
    [
        ("kb_swing", {"name": "Kettlebell Swing"}, "One-Arm_Kettlebell_Swings", "Two-Arm_Kettlebell_Swing"),
        ("my_ht", {"name": "Bodyweight Hip Thrust"}, "Barbell_Hip_Thrust", "Bodyweight_Hip_Thrust"),
        ("x", {"name": "Goblet Squats"}, "Goblet_Squat", "Goblet_Squat"),  # über die Katalog-ID
        ("x", {"name": "Unbekannt", "aliases": ["Walk"]}, None, "Brisk_Walk"),  # Name aus den Vorlagen
        ("x", {"name": "Plank", "image": False}, "Plank", None),
        ("x", {"name": "Zirkeltraining Spezial"}, None, None),
        ("x", {"name": "Etwas", "image": "Plank"}, None, "Plank"),
    ],
)
def test_picto_match(ex_id, ex, catalog_id, expected):
    assert PICTOS.match(ex_id, ex, catalog_id) == expected


def test_single_images():
    assert "Brisk_Walk" in PICTOS.single()
    assert "Goblet_Squat" not in PICTOS.single()
