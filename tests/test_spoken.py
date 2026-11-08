import pytest

from custom_components.training_assistant.spoken import parse_answer, word_to_number


@pytest.mark.parametrize(
    ("word", "value"),
    [("acht", 8), ("zwölf", 12), ("einundzwanzig", 21), ("zwölfeinhalb", 12.5), ("anderthalb", 1.5),
     ("hundertzwanzig", 120), ("zwanzig", 20), ("quatsch", None)],
)
def test_word_to_number(word, value):
    assert word_to_number(word) == value


@pytest.mark.parametrize(
    ("text", "kind", "reps", "weight"),
    [
        ("ja", "confirm", None, None),
        ("Ja, wie geplant", "confirm", None, None),
        ("8 Wiederholungen 15 Kilo", "correct", 8, 15),
        ("acht mal fünfzehn", "correct", 8, 15),
        ("zehn mal zwölfeinhalb Kilo", "correct", 10, 12.5),
        ("zwölf komma fünf kilo und sechs", "correct", 6, 12.5),
        ("nur sechs", "correct", 6, None),
        ("8x15", "correct", 8, 15),
        ("übersprungen", "skip", None, None),
        ("", "unknown", None, None),
        (None, "unknown", None, None),
        ("ein bisschen schwer", "confirm", None, None),
    ],
)
def test_parse_answer(text, kind, reps, weight):
    result = parse_answer(text)
    assert result["kind"] == kind
    assert result["reps"] == reps
    assert result["weight_kg"] == weight


def test_parse_answer_timed():
    assert parse_answer("fünfundvierzig Sekunden", timed=True)["duration_s"] == 45
    assert parse_answer("40", timed=True)["duration_s"] == 40


@pytest.mark.parametrize(
    ("text", "kind", "reps", "weight"),
    [
        ("yes", "confirm", None, None),
        ("yeah, as planned", "confirm", None, None),
        ("eight times fifteen", "correct", 8, 15),
        ("8 reps 15 kilos", "correct", 8, 15),
        ("ten reps with twelve and a half kilos", "correct", 10, 12.5),
        ("twelve point five kilos and six", "correct", 6, 12.5),
        ("only six", "correct", 6, None),
        ("twenty-five", "correct", 25, None),
        ("twenty five times forty", "correct", 25, 40),
        ("skipped", "skip", None, None),
        ("a bit heavy", "confirm", None, None),
    ],
)
def test_parse_answer_english(text, kind, reps, weight):
    result = parse_answer(text, lang="en")
    assert (result["kind"], result["reps"], result["weight_kg"]) == (kind, reps, weight)


def test_parse_answer_english_timed():
    assert parse_answer("forty five seconds", timed=True, lang="en")["duration_s"] == 45


@pytest.mark.parametrize(
    ("text", "lang", "kind", "reps", "effort"),
    [
        ("ja, war locker", "de", "confirm", None, "easy"),
        ("acht, war schwer", "de", "correct", 8, "hard"),
        ("ja", "de", "confirm", None, None),
        ("yes, easy", "en", "confirm", None, "easy"),
        ("only six, that was tough", "en", "correct", 6, "hard"),
        ("skip", "en", "skip", None, None),
    ],
)
def test_effort(text, lang, kind, reps, effort):
    res = parse_answer(text, lang=lang)
    assert (res["kind"], res["reps"], res["effort"]) == (kind, reps, effort)
