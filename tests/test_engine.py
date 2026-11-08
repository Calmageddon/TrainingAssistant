from pathlib import Path

import yaml

from custom_components.training_assistant.engine import Engine, edit_set, new_session
from custom_components.training_assistant.plan import build_steps

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
NOW = "2026-11-07T10:00:00+00:00"


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def session(name="ganzkoerper.yaml", workout="a"):
    path = FIXTURES / name if (FIXTURES / name).exists() else EXAMPLES / name
    plan = yaml.safe_load(path.read_text())
    w = next(x for x in plan["workouts"] if x["id"] == workout)
    state = new_session(session_id="s1", plan=plan, plan_id="p", workout=w,
                        steps=build_steps(plan, workout), satellite="assist_satellite.x", now=NOW, lang="de")
    eng = Engine(state)
    return eng, eng.start()


def kinds(effects):
    return [e["kind"] for e in effects]


def texts(effects):
    return " ".join(e["text"] for e in effects if e["kind"] in ("announce", "ask"))


def test_full_run_with_button_only():
    eng, eff = session()
    assert "Aufwärmen" in texts(eff)
    presses = 0
    while not eng.finished:
        eff = eng.press_next(NOW)
        # Rückfrage sofort per Knopf bestätigen
        if eng.s["pending_question"] is None:
            for e in eff:
                if e["kind"] == "ask":
                    eng.question_started(e["set_id"])
            if eng.s["pending_question"] is not None:
                eng.press_next(NOW)
        presses += 1
        assert presses < 200
    assert eng.s["status"] == "finished"
    assert len(eng.s["sets"]) == 12
    assert all(s["status"] == "confirmed" for s in eng.s["sets"])
    assert eng.s["sets"][1]["weight_kg"] == 16


def test_ready_then_sets_and_rest():
    eng, _ = session()
    eff = eng.press_next(NOW)  # Aufwärmen fertig
    assert eng.s["phase"] == "ready" and "3 Runden" in texts(eff)
    eff = eng.press_next(NOW)  # bereit
    assert eng.s["phase"] == "active" and "Push-Ups" in texts(eff)
    eff = eng.press_next(NOW)  # Satz 1 fertig
    assert kinds(eff)[1] == "ask"
    assert any(e["kind"] == "rest" and e["seconds"] == 30 for e in eff)
    assert "Goblet Squats" in texts(eff)


def test_answer_corrects_set():
    eng, _ = session()
    eng.press_next(NOW)
    eng.press_next(NOW)
    eff = eng.press_next(NOW)
    set_id = next(e["set_id"] for e in eff if e["kind"] == "ask")
    eng.question_started(set_id)
    eng.answer(set_id, {"kind": "correct", "reps": 6, "weight_kg": None, "duration_s": None}, NOW)
    rec = eng.find_set(set_id)
    assert rec["reps"] == 6 and rec["status"] == "corrected"
    assert eng.s["pending_question"] is None


def test_undo_restores_previous_set():
    eng, _ = session()
    eng.press_next(NOW)
    eng.press_next(NOW)
    eng.press_next(NOW)  # Push-Ups erfasst
    assert len(eng.s["sets"]) == 1
    eng.undo(NOW)
    assert len(eng.s["sets"]) == 0 and eng.step["exercise"] == "push_up" and eng.s["phase"] == "active"
    eng.undo(NOW)
    assert eng.s["phase"] == "ready"


def test_skip_block_and_interval():
    eng, _ = session()
    eng.press_next(NOW)  # Aufwärmen
    eng.skip(NOW)  # ganzen Zirkel überspringen
    assert eng.step["type"] == "interval" and eng.s["phase"] == "ready"
    assert len([s for s in eng.s["sets"] if s["status"] == "skipped"]) == 12
    eff = eng.press_next(NOW)
    assert "interval_start" in kinds(eff) and eng.s["phase"] == "interval"
    eng.interval_done()
    assert eng.step["type"] == "cooldown"


def test_pause_toggle():
    eng, _ = session()
    assert "pause" in kinds(eng.toggle_pause(NOW))
    assert "resume" in kinds(eng.press_next(NOW))  # Knopf in der Pause = fortsetzen


def test_total_reps_block_ends_early():
    eng, _ = session("feature-testplan.yaml", "w4")
    # bis zum Pull-Up-Block vorspulen
    while eng.step["block_name"] != "Pull-Up-Finisher":
        eng.skip(NOW) if eng.s["phase"] == "ready" else eng.press_next(NOW)
        eng.s["pending_question"] = None
    eng.press_next(NOW)  # bereit
    for reps in (8, 7, 6):
        eff = eng.press_next(NOW)
        set_id = next(e["set_id"] for e in eff if e["kind"] == "ask") if any(
            e["kind"] == "ask" for e in eff) else eng.s["sets"][-1]["id"]
        eng.question_started(set_id)
        eng.answer(set_id, {"kind": "correct", "reps": reps}, NOW)
        if eng.step["block_name"] != "Pull-Up-Finisher":
            break
    assert sum(s["reps"] for s in eng.s["sets"] if s["exercise"] == "pull_up") == 21
    assert eng.step["type"] == "cooldown"


def test_time_cap_block():
    plan = {
        "schema_version": 1, "name": "T", "exercises": {"a": {"name": "A"}, "b": {"name": "B"}},
        "workouts": [{"id": "w", "name": "W", "blocks": [
            {"type": "circuit", "time_cap_s": 300, "exercises": [{"exercise": "a", "reps": 5}, {"exercise": "b", "reps": 5}]},
            {"type": "cooldown"}]}],
    }
    state = new_session(session_id="s", plan=plan, plan_id="t", workout=plan["workouts"][0],
                        steps=build_steps(plan, "w"), satellite=None, now=NOW, lang="de")
    eng = Engine(state)
    eng.start()
    eff = eng.press_next(NOW)
    assert {"kind": "block_timer", "seconds": 300} in eff
    for _ in range(5):
        eng.press_next(NOW)
    assert eng.step["round"] == 3 and eng.step["exercise"] == "b"
    assert "Runde 4. A" in texts(eng.press_next(NOW))  # offene Runden: ohne „von …“
    eng.s["block_expired"] = True
    eng.press_next(NOW)
    assert eng.step["type"] == "cooldown"


def test_edit_set():
    sets = [{"id": 1, "reps": 8, "weight_kg": 10, "duration_s": None, "status": "planned"}]
    edit_set(sets, 1, {"reps": 9})
    assert sets[0]["reps"] == 9 and sets[0]["status"] == "edited"


def to_first_set(name="ganzkoerper.yaml", workout="b"):
    eng, _ = session(name, workout)
    eng.press_next(NOW)  # Aufwärmen
    eng.press_next(NOW)  # bereit
    return eng


def test_actual_values_logged_without_question():
    eng = to_first_set()  # Rumänisches Kreuzheben 5x5 mit 20 kg
    eff = eng.press_next(NOW, {"reps": 4, "weight_kg": 17.5})
    rec = eng.s["sets"][-1]
    assert (rec["reps"], rec["weight_kg"], rec["status"]) == (4, 17.5, "corrected")
    assert "ask" not in kinds(eff)


def test_reduced_weight_carries_to_remaining_sets():
    eng = to_first_set()
    eff = eng.press_next(NOW, {"reps": 5, "weight_kg": 17.5})
    rdl = [s for s in eng.steps if s.get("exercise") == "romanian_deadlift"]
    assert all(s["target_weight"] == 17.5 for s in rdl[1:])
    assert "17,5 Kilo" in texts(eff)  # nächste Ansage nennt das neue Gewicht
    other = next(s for s in eng.steps if s.get("exercise") == "dumbbell_press")
    assert other["target_weight"] == 12


def test_actual_equal_to_plan_is_confirmed():
    eng = to_first_set()
    eng.press_next(NOW, {"reps": 5, "weight_kg": 20})
    assert eng.s["sets"][-1]["status"] == "confirmed"


def test_actual_with_pending_question_confirms_and_logs():
    eng = to_first_set()
    eff = eng.press_next(NOW)  # Satz 1 per Knopf → Rückfrage offen
    eng.question_started(next(e["set_id"] for e in eff if e["kind"] == "ask"))
    eng.press_next(NOW, {"reps": 3, "weight_kg": 20})  # Karte: Satz 2 mit echten Werten
    assert [s["status"] for s in eng.s["sets"]] == ["confirmed", "corrected"]
    assert eng.s["sets"][1]["reps"] == 3 and eng.s["pending_question"] is None


def test_voice_correction_carries_weight():
    eng = to_first_set()
    eff = eng.press_next(NOW)
    set_id = next(e["set_id"] for e in eff if e["kind"] == "ask")
    eng.question_started(set_id)
    eng.answer(set_id, {"kind": "correct", "reps": 5, "weight_kg": 15}, NOW)
    assert eng.step["target_weight"] == 15


def test_english_announcements():
    plan = yaml.safe_load((EXAMPLES / "ganzkoerper.yaml").read_text())
    w = next(x for x in plan["workouts"] if x["id"] == "b")
    state = new_session(session_id="s", plan=plan, plan_id="p", workout=w, steps=build_steps(plan, "b"),
                        satellite="assist_satellite.x", now=NOW, lang="en")
    eng = Engine(state)
    assert "Start with your warm-up" in texts(eng.start())
    eff = eng.press_next(NOW)  # Aufwärmen fertig → Block-Ansage
    assert "5 sets, 5 reps with 20 kilos" in texts(eff) and "Press the button" in texts(eff)
    eng.press_next(NOW)
    eff = eng.press_next(NOW)
    assert "5 reps with 20 kilos as planned?" in texts(eff)
    assert "Rest 120 seconds." in texts(eff)


def test_old_sessions_default_to_german():
    eng, eff = session()
    eng.s.pop("lang")
    assert Engine(eng.s).sp.lang == "de"


def test_flow_segments_logged_as_sets():
    from custom_components.training_assistant.phrases import Speech

    plan = {
        "schema_version": 1, "name": "Flow", "exercises": {"dog": {"name": "Hund"}, "tree": {"name": "Baum"}},
        "workouts": [{"id": "w", "name": "W", "blocks": [
            {"type": "flow", "exercises": [{"exercise": "dog", "duration_s": 30},
                                           {"exercise": "tree", "duration_s": 20, "per_side": True}]},
            {"type": "cooldown"}]}],
    }
    w = plan["workouts"][0]
    state = new_session(session_id="s1", plan=plan, plan_id="p", workout=w, steps=build_steps(plan, "w"),
                        satellite=None, now=NOW, lang="de")
    eng = Engine(state)
    eng.start()
    assert "3 Abschnitte" in eng.sp.describe_block(eng.steps, 0)
    eng.press_next(NOW)  # Flow starten
    assert eng.s["phase"] == "interval"
    for i, seg in enumerate(eng.step["segments"], 1):
        eng.log_segment({**seg, "index": i, "count": 3}, NOW)
    sets = eng.s["sets"]
    assert [(x["exercise"], x["duration_s"], x.get("side")) for x in sets] == [
        ("dog", 30, None), ("tree", 20, "left"), ("tree", 20, "right")]
    assert Speech("de").segment_name(eng.step["segments"][1]) == "Baum, linke Seite"
    effects = eng.interval_done()
    assert any(e["kind"] == "announce" and "Flow geschafft" in e["text"] for e in effects)
    assert eng.step["type"] == "cooldown"
