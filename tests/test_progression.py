from custom_components.training_assistant.progression import suggest

DOUBLE = {"type": "double", "increment_kg": 2.5}
LINEAR = {"type": "linear", "increment_kg": 2}


def sets(*pairs, status="confirmed"):
    return [{"reps": r, "weight_kg": w, "status": status} for r, w in pairs]


def test_no_history_uses_plan():
    s = suggest([], rep_range=(8, 12), progression=DOUBLE, plan_weight=16)
    assert (s["weight_kg"], s["reps"], s["increased"]) == (16, 8, False)


def test_double_all_at_top_increases_weight():
    s = suggest(sets((12, 16), (12, 16), (12, 16)), rep_range=(8, 12), progression=DOUBLE, plan_weight=16)
    assert (s["weight_kg"], s["reps"], s["increased"]) == (18.5, 8, True)


def test_double_aims_one_more_rep():
    s = suggest(sets((10, 16), (9, 16), (8, 16)), rep_range=(8, 12), progression=DOUBLE, plan_weight=16)
    assert (s["weight_kg"], s["reps"]) == (16, 9)


def test_double_uses_lowest_weight():
    s = suggest(sets((12, 18), (12, 16)), rep_range=(8, 12), progression=DOUBLE, plan_weight=16)
    assert s["weight_kg"] == 18.5


def test_linear():
    assert suggest(sets((5, 60), (5, 60)), rep_range=(5, 5), progression=LINEAR, plan_weight=60)["weight_kg"] == 62
    assert suggest(sets((5, 60), (4, 60)), rep_range=(5, 5), progression=LINEAR, plan_weight=60)["weight_kg"] == 60


def test_skipped_sets_ignored():
    hist = sets((12, 16)) + [{"reps": None, "weight_kg": None, "status": "skipped"}]
    assert suggest(hist, rep_range=(8, 12), progression=DOUBLE, plan_weight=16)["increased"]


def test_bodyweight_double_top():
    s = suggest(sets((15, None)), rep_range=(12, 15), progression=DOUBLE, plan_weight=None)
    assert s["weight_kg"] is None and "Zusatzgewicht" in s["reason"]


REPS = {"type": "reps", "increment": 1}


def bw(*reps, target):
    return [{"reps": r, "weight_kg": None, "target_reps": target, "status": "confirmed"} for r in reps]


def test_reps_all_done_adds_one():
    s = suggest(bw(12, 12, 12, target=12), rep_range=(12, 12), progression=REPS, plan_weight=None)
    assert (s["reps"], s["increased"], s["weight_kg"]) == (13, True, None)


def test_reps_builds_on_last_target_not_plan():
    s = suggest(bw(14, 14, 14, target=14), rep_range=(12, 12), progression=REPS, plan_weight=None)
    assert s["reps"] == 15


def test_reps_missed_keeps_target():
    s = suggest(bw(13, 12, 11, target=13), rep_range=(12, 12), progression=REPS, plan_weight=None)
    assert (s["reps"], s["increased"]) == (13, False)


def test_reps_cap_reached():
    prog = {"type": "reps", "max_reps": 20}
    assert suggest(bw(19, 19, target=19), rep_range=(12, 12), progression=prog, plan_weight=None)["reps"] == 20
    s = suggest(bw(20, 20, target=20), rep_range=(12, 12), progression=prog, plan_weight=None)
    assert s["reps"] == 20 and "schwerere Variante" in s["reason"]


def test_reps_range_caps_at_top_and_increment():
    prog = {"type": "reps", "increment": 2}
    assert suggest(bw(11, 11, target=11), rep_range=(8, 12), progression=prog, plan_weight=None)["reps"] == 12


def test_reps_without_stored_target_uses_plan_min():
    hist = [{"reps": 12, "weight_kg": None, "status": "confirmed"}] * 3
    assert suggest(hist, rep_range=(12, 12), progression=REPS, plan_weight=None)["reps"] == 13


def test_effort_hard_holds_and_easy_doubles():
    from custom_components.training_assistant.progression import suggest as sug

    def sets(reps, effort, w=20):
        return [{"reps": r, "weight_kg": w, "status": "confirmed", "effort": effort} for r in reps]

    dbl = {"type": "double", "increment_kg": 2.5}
    assert sug(sets([9, 9, 9], None), rep_range=(8, 12), progression=dbl, plan_weight=20)["reps"] == 10
    easy = sug(sets([9, 9, 9], "easy"), rep_range=(8, 12), progression=dbl, plan_weight=20)
    assert easy["reps"] == 11 and easy["reason_key"] == "easy_target"
    hard = sug(sets([12, 12, 12], "hard"), rep_range=(8, 12), progression=dbl, plan_weight=20)
    assert hard["weight_kg"] == 20 and hard["reason_key"] == "hard_hold"
    lin = {"type": "linear", "increment_kg": 2.5}
    assert sug(sets([5] * 5, "easy"), rep_range=(5, 5), progression=lin, plan_weight=20)["weight_kg"] == 25
    mixed = sets([5] * 4, None) + sets([5], "hard")
    assert sug(mixed, rep_range=(5, 5), progression=lin, plan_weight=20)["reason_key"] == "hard_hold"
