"""Ablauf einer Trainings-Session als reine Zustandsmaschine.

Die Engine ändert nur den Zustand (ein dict, das direkt gespeichert wird) und gibt
eine Liste von „Effekten“ zurück, die der Manager ausführt:

    {"kind": "announce", "text": ...}            Ansage über den Satelliten
    {"kind": "ask", "set_id": ..., "text": ...}  Rückfrage nach einem Satz
    {"kind": "rest", "seconds": n}               Pausentimer starten
    {"kind": "rest_cancel"}                      Pausentimer stoppen
    {"kind": "interval_start"}                   HIIT-Block zeitgesteuert starten
    {"kind": "interval_stop"}                    HIIT-Block abbrechen
    {"kind": "block_timer", "seconds": n}        Zeitlimit eines Blocks starten
    {"kind": "block_timer_cancel"}               Zeitlimit stoppen
    {"kind": "pause"} / {"kind": "resume"}       Timer anhalten / fortsetzen
    {"kind": "event", "type": ..., "data": {}}   HA-Event für Automationen
    {"kind": "finished"}                         Session abschließen und speichern

Ohne Home-Assistant-Abhängigkeiten.
"""

from __future__ import annotations

from typing import Any

from .const import (
    PHASE_ACTIVE,
    PHASE_FINISHED,
    PHASE_INTERVAL,
    PHASE_READY,
    SET_CONFIRMED,
    SET_CORRECTED,
    SET_EDITED,
    SET_PENDING,
    SET_PLANNED,
    SET_SKIPPED,
    SET_UNCONFIRMED,
)

from .phrases import Speech

Effects = list[dict[str, Any]]


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


def new_session(
    *,
    session_id: str,
    plan: dict,
    plan_id: str,
    workout: dict,
    steps: list[dict],
    satellite: str | None,
    now: str,
    lang: str = "en",
) -> dict[str, Any]:
    return {
        "lang": lang,
        "id": session_id,
        "plan_id": plan_id,
        "plan_name": plan["name"],
        "workout_id": workout["id"],
        "workout_name": workout["name"],
        "started_at": now,
        "finished_at": None,
        "status": "running",
        "satellite": satellite,
        "steps": steps,
        "idx": 0,
        "phase": PHASE_READY,
        "paused": False,
        "sets": [],
        "next_set_id": 1,
        "pending_question": None,
        "rest_until": None,
        "interval": None,
        "block_expired": False,
    }


class Engine:
    """Arbeitet auf einem Session-dict (wird in-place geändert)."""

    def __init__(self, state: dict[str, Any]) -> None:
        self.s = state
        # Trainings von vor der Mehrsprachigkeit waren Deutsch
        self.sp = Speech(state.get("lang", "de"))

    # -- Hilfen ------------------------------------------------------------

    @property
    def steps(self) -> list[dict]:
        return self.s["steps"]

    @property
    def step(self) -> dict | None:
        idx = self.s["idx"]
        return self.steps[idx] if 0 <= idx < len(self.steps) else None

    @property
    def finished(self) -> bool:
        return self.s["phase"] == PHASE_FINISHED

    def _block_start(self, idx: int) -> bool:
        return idx == 0 or self.steps[idx - 1]["block"] != self.steps[idx]["block"]

    def _next_block(self, idx: int) -> int:
        """Index des ersten Schritts nach dem Block von `idx`."""
        block = self.steps[idx]["block"]
        while idx < len(self.steps) and self.steps[idx]["block"] == block:
            idx += 1
        return idx

    def _block_done(self, step: dict) -> str | None:
        """Ist ein offener Block fertig? Liefert den Grund als Ansagetext."""
        end = step.get("block_end") or {}
        if end.get("time_cap_s") and self.s.get("block_expired"):
            return self.sp.t("time_up")
        if end.get("total_reps"):
            total = sum(x["reps"] or 0 for x in self.s["sets"]
                        if x["block"] == step["block"] and x.get("reps") is not None)
            if total >= end["total_reps"]:
                return self.sp.t("total_reached", n=end["total_reps"])
        return None

    def _event(self, etype: str, **data: Any) -> dict:
        return {"kind": "event", "type": etype, "data": data}

    def find_set(self, set_id: int) -> dict | None:
        return next((x for x in self.s["sets"] if x["id"] == set_id), None)

    # -- Schritte betreten -------------------------------------------------

    def start(self) -> Effects:
        effects: Effects = [self._event("session_started", workout=self.s["workout_name"])]
        intro = self.sp.t("intro", w=self.s["workout_name"])
        effects += self._enter(0, intro=intro)
        return effects

    def _enter(self, idx: int, *, intro: str = "", rest_s: int = 0) -> Effects:
        self.s["idx"] = idx
        self.s["interval"] = None
        if idx >= len(self.steps):
            return self._finish(completed=True)
        step = self.steps[idx]
        prefix = intro
        effects: Effects = []
        if self._block_start(idx):
            self.s["block_expired"] = False
            effects.append({"kind": "block_timer_cancel"})
        if rest_s:
            prefix = f"{prefix} {self.sp.t('rest', s=rest_s)}".strip()
        if step["type"] in ("warmup", "cooldown"):
            self.s["phase"] = PHASE_ACTIVE
            text = self.sp.t("warmup" if step["type"] == "warmup" else "cooldown")
            if step.get("note"):
                text = f"{text} {step['note']}"
            effects.append({"kind": "announce", "text": f"{prefix} {text}".strip()})
        elif self._block_start(idx):
            self.s["phase"] = PHASE_READY
            effects.append({"kind": "announce", "text": f"{prefix} {self.sp.describe_block(self.steps, idx)}".strip()})
        else:
            self.s["phase"] = PHASE_ACTIVE
            effects.append({"kind": "announce",
                            "text": f"{prefix} {self.sp.t('next', d=self.sp.describe_step(step))}".strip()})
        effects.append(self._event("step", idx=idx, phase=self.s["phase"], block=self.sp.block_name(step),
                                   exercise=step.get("exercise_name")))
        return effects

    def _finish(self, *, completed: bool) -> Effects:
        self.s["phase"] = PHASE_FINISHED
        self.s["status"] = "finished" if completed else "aborted"
        self.s["rest_until"] = None
        self.s["interval"] = None
        done = [x for x in self.s["sets"] if x["status"] != SET_SKIPPED]
        text = self.sp.t("finished", n=len(done))
        return [
            {"kind": "rest_cancel"},
            {"kind": "announce", "text": text},
            self._event("session_finished", sets=len(done), completed=completed),
            {"kind": "finished"},
        ]

    # -- Satz erfassen -----------------------------------------------------

    def _log(self, step: dict, *, status: str, reps: int | None = None, weight: float | None = None,
             duration: int | None = None, now: str) -> dict:
        planned = status == SET_PLANNED
        rec = {
            "id": self.s["next_set_id"],
            "step": step["idx"],
            "block": step["block"],
            "block_name": step["block_name"],
            "exercise": step["exercise"],
            "exercise_name": step["exercise_name"],
            "round": step.get("round"),
            "set_no": step.get("set_no"),
            "sets": step.get("sets"),
            "rep_range": step.get("rep_range"),
            "target_reps": step.get("target_reps"),
            "target_weight": step.get("target_weight"),
            "target_duration": step.get("target_duration"),
            "amrap": step.get("amrap", False),
            "hold_max": step.get("hold_max", False),
            "per_side": step.get("per_side", False),
            "reps": step.get("target_reps") if planned else reps,
            "weight_kg": step.get("target_weight") if planned else weight,
            "duration_s": step.get("target_duration") if planned else duration,
            "status": status,
            "ts": now,
        }
        if status == SET_SKIPPED:
            rec["reps"] = rec["weight_kg"] = rec["duration_s"] = None
        self.s["next_set_id"] += 1
        self.s["sets"].append(rec)
        return rec

    # -- Bedienung ---------------------------------------------------------

    def _carry_weight(self, rec: dict) -> None:
        """Geändertes Gewicht gilt für die restlichen Sätze dieser Übung in dieser Session."""
        weight = rec.get("weight_kg")
        if weight is None or weight == rec.get("target_weight"):
            return
        for step in self.steps[rec["step"] + 1:]:
            if step.get("exercise") == rec["exercise"] and step.get("target_weight") is not None:
                step["target_weight"] = weight

    def press_next(self, now: str, actual: dict[str, Any] | None = None) -> Effects:
        """Knopf „Weiter“.

        `actual` (von der Karte): tatsächliche Werte {reps, weight_kg, duration_s} für den
        aktuellen Satz. Dann wird ohne Rückfrage gespeichert.
        """
        if self.finished:
            return []
        if self.s["paused"]:
            return self.toggle_pause(now)
        pre: Effects = []
        if self.s["pending_question"] is not None:
            # Knopf während der Rückfrage = „ja, wie geplant“
            pre = self.answer(self.s["pending_question"], {"kind": "confirm"}, now)
            if actual is None or self.s["phase"] != PHASE_ACTIVE or not self.step or self.step["type"] != "set":
                return pre

        step = self.step
        phase = self.s["phase"]
        if phase == PHASE_READY:
            if step["type"] == "interval":
                self.s["phase"] = PHASE_INTERVAL
                return [{"kind": "interval_start"}, self._event("step", idx=step["idx"], phase=PHASE_INTERVAL,
                                                                 block=self.sp.block_name(step), exercise=None)]
            self.s["phase"] = PHASE_ACTIVE
            cap = (step.get("block_end") or {}).get("time_cap_s")
            timer = [{"kind": "block_timer", "seconds": cap}] if cap else []
            return timer + [
                {"kind": "announce", "text": self.sp.t("go", d=self.sp.describe_step(step))},
                self._event("step", idx=step["idx"], phase=PHASE_ACTIVE, block=self.sp.block_name(step),
                            exercise=step.get("exercise_name")),
            ]
        if phase == PHASE_INTERVAL:
            return [{"kind": "interval_stop"}, *self._enter(step["idx"] + 1)]

        # aktiv
        effects: Effects = [*pre, {"kind": "rest_cancel"}]
        rest = 0
        if step["type"] == "set":
            if actual:
                values = {
                    "reps": actual.get("reps", step.get("target_reps")),
                    "weight": actual.get("weight_kg", step.get("target_weight")),
                    "duration": actual.get("duration_s", step.get("target_duration")),
                }
                same = (values["reps"] == step.get("target_reps") and values["weight"] == step.get("target_weight")
                        and values["duration"] == step.get("target_duration"))
                rec = self._log(step, status=SET_CONFIRMED if same else SET_CORRECTED, now=now, **values)
                if actual.get("effort"):
                    rec["effort"] = actual["effort"]
                self._carry_weight(rec)
            else:
                rec = self._log(step, status=SET_PLANNED, now=now)
                question = self.sp.question(rec)
                if question:
                    effects.append({"kind": "ask", "set_id": rec["id"], "text": question})
            effects.append(self._event("set_logged", set_id=rec["id"], exercise=rec["exercise_name"],
                                       reps=rec["reps"], weight_kg=rec["weight_kg"]))
            rest = step.get("rest_after_s") or 0
            reason = self._block_done(step)
            if reason:
                effects.append({"kind": "block_timer_cancel"})
                block_rest = step.get("block_rest_s") or 0
                effects += self._enter(self._next_block(step["idx"]), intro=reason, rest_s=block_rest)
                if block_rest and not self.finished:
                    effects.append({"kind": "rest", "seconds": block_rest})
                return effects
        effects += self._enter(step["idx"] + 1, rest_s=rest)
        if rest and not self.finished:
            effects.append({"kind": "rest", "seconds": rest})
        return effects

    def log_segment(self, seg: dict, now: str) -> dict | None:
        """Abgeschlossenen Zeitabschnitt (HIIT/Flow) als Satz mit Dauer speichern."""
        step = self.step
        if not step or step["type"] != "interval" or not seg.get("exercise"):
            return None
        pseudo = {
            "idx": step["idx"], "block": step["block"], "block_name": step.get("block_name"),
            "exercise": seg["exercise"], "exercise_name": seg["name"], "round": seg.get("index"),
            "sets": None, "set_no": None, "rounds": seg.get("count"), "rep_range": None, "target_reps": None,
            "target_weight": None, "target_duration": seg["work_s"], "per_side": bool(seg.get("side")),
        }
        rec = self._log(pseudo, status=SET_CONFIRMED, duration=seg["work_s"], now=now)
        if seg.get("side"):
            rec["side"] = seg["side"]
        return rec

    def interval_done(self) -> Effects:
        """Vom Manager aufgerufen, wenn der HIIT-/Flow-Block abgelaufen ist."""
        if self.s["phase"] != PHASE_INTERVAL:
            return []
        rest = self.step.get("block_rest_s") or 0
        done = self.sp.t("flow_done" if self.step.get("block_type") == "flow" else "hiit_done")
        effects = [self._event("interval_done"), *self._enter(self.s["idx"] + 1, intro=done, rest_s=rest)]
        if rest and not self.finished:
            effects.append({"kind": "rest", "seconds": rest})
        return effects

    def undo(self, now: str) -> Effects:
        """Knopf „Rückgängig“: einen Schritt zurück, dort erfassten Satz verwerfen."""
        idx, phase = self.s["idx"], self.s["phase"]
        effects: Effects = [{"kind": "rest_cancel"}]
        if phase == PHASE_INTERVAL:
            self.s["phase"] = PHASE_READY
            self.s["interval"] = None
            return [{"kind": "interval_stop"}, {"kind": "announce", "text": self.sp.describe_block(self.steps, idx)}]
        if phase == PHASE_ACTIVE and idx < len(self.steps) and self.steps[idx]["type"] in ("set",) \
                and self._block_start(idx):
            self.s["phase"] = PHASE_READY
            return effects + [{"kind": "announce", "text": self.sp.describe_block(self.steps, idx)}]
        prev = (len(self.steps) if phase == PHASE_FINISHED else idx) - 1
        if prev < 0:
            return []
        if phase == PHASE_FINISHED:
            self.s["status"] = "running"
            self.s["finished_at"] = None
        removed = [x for x in self.s["sets"] if x["step"] == prev]
        self.s["sets"] = [x for x in self.s["sets"] if x["step"] != prev]
        if self.s["pending_question"] in {x["id"] for x in removed}:
            self.s["pending_question"] = None
        self.s["idx"] = prev
        step = self.steps[prev]
        if step["type"] == "interval":
            self.s["phase"] = PHASE_READY
            text = self.sp.describe_block(self.steps, prev)
        else:
            self.s["phase"] = PHASE_ACTIVE
            text = self.sp.t("back", d=self.sp.describe_step(step) if step["type"] == "set"
                             else self.sp.block_name(step) + ".")
        effects.append({"kind": "announce", "text": text})
        effects.append(self._event("undo", idx=prev))
        return effects

    def skip(self, now: str) -> Effects:
        """Knopf „Überspringen“: aktuellen Satz auslassen, bzw. ganzen Block, wenn er noch nicht begonnen hat."""
        if self.finished:
            return []
        step = self.step
        effects: Effects = [{"kind": "rest_cancel"}]
        if self.s["phase"] == PHASE_INTERVAL:
            effects.append({"kind": "interval_stop"})
        if self.s["phase"] == PHASE_READY:
            nxt = step["idx"]
            while nxt < len(self.steps) and self.steps[nxt]["block"] == step["block"]:
                if self.steps[nxt]["type"] == "set":
                    self._log(self.steps[nxt], status=SET_SKIPPED, now=now)
                nxt += 1
            return effects + self._enter(nxt, intro=self.sp.t("block_skipped", name=self.sp.block_name(step)))
        if step["type"] == "set":
            self._log(step, status=SET_SKIPPED, now=now)
        return effects + self._enter(step["idx"] + 1, intro=self.sp.t("skipped"))

    def toggle_pause(self, now: str) -> Effects:
        if self.finished:
            return []
        self.s["paused"] = not self.s["paused"]
        if self.s["paused"]:
            return [{"kind": "pause"}, {"kind": "announce", "text": self.sp.t("paused")},
                    self._event("paused")]
        return [{"kind": "resume"}, {"kind": "announce", "text": self.sp.t("resumed")},
                self._event("resumed")]

    def finish(self, now: str, *, completed: bool = True) -> Effects:
        if self.finished:
            return []
        effects: Effects = [{"kind": "interval_stop"}] if self.s["phase"] == PHASE_INTERVAL else []
        return effects + self._finish(completed=completed)

    # -- Antworten und Korrekturen ------------------------------------------

    def question_started(self, set_id: int) -> None:
        rec = self.find_set(set_id)
        if rec is not None and rec["status"] == SET_PLANNED:
            rec["status"] = SET_PENDING
            self.s["pending_question"] = set_id

    def answer(self, set_id: int, parsed: dict[str, Any], now: str) -> Effects:
        """Ergebnis einer Rückfrage übernehmen (siehe spoken.parse_answer)."""
        if self.s["pending_question"] == set_id:
            self.s["pending_question"] = None
        rec = self.find_set(set_id)
        if rec is None or rec["status"] not in (SET_PENDING, SET_PLANNED):
            return []
        kind = parsed.get("kind")
        if parsed.get("effort") and kind in ("confirm", "correct"):
            rec["effort"] = parsed["effort"]
        if kind == "confirm":
            rec["status"] = SET_CONFIRMED
        elif kind == "correct":
            for key in ("reps", "weight_kg", "duration_s"):
                if parsed.get(key) is not None:
                    rec[key] = parsed[key]
            rec["status"] = SET_CORRECTED
            self._carry_weight(rec)
        elif kind == "skip":
            rec["status"] = SET_SKIPPED
            rec["reps"] = rec["weight_kg"] = rec["duration_s"] = None
        else:
            rec["status"] = SET_UNCONFIRMED
        effects: Effects = [self._event("set_answered", set_id=set_id, status=rec["status"], reps=rec["reps"],
                                        weight_kg=rec["weight_kg"])]
        return effects + self.check_block_end()

    def check_block_end(self) -> Effects:
        """Gesamtwiederholungen nachträglich erreicht (Antwort/Korrektur)? Dann zum nächsten Block."""
        step = self.step
        if (not step or step["type"] != "set" or self.s["phase"] != PHASE_ACTIVE
                or not (step.get("block_end") or {}).get("total_reps")):
            return []
        reason = self._block_done(step)
        if not reason:
            return []
        rest = step.get("block_rest_s") or 0
        effects: Effects = [{"kind": "rest_cancel"}, *self._enter(self._next_block(step["idx"]), intro=reason,
                                                                   rest_s=rest)]
        if rest and not self.finished:
            effects.append({"kind": "rest", "seconds": rest})
        return effects


def edit_set(sets: list[dict], set_id: int, changes: dict[str, Any]) -> dict:
    """Satz nachträglich ändern (Karte). Wirft KeyError, wenn es ihn nicht gibt."""
    rec = next((x for x in sets if x["id"] == set_id), None)
    if rec is None:
        raise KeyError(set_id)
    for key in ("reps", "weight_kg", "duration_s"):
        if key in changes:
            rec[key] = changes[key]
    if "effort" in changes:
        # Nur die Anstrengung geändert: Status (bestätigt/korrigiert) bleibt
        rec["effort"] = changes["effort"] if changes["effort"] in ("easy", "hard") else None
        if set(changes) <= {"effort"}:
            return rec
    if changes.get("skipped"):
        rec["status"] = SET_SKIPPED
        rec["reps"] = rec["weight_kg"] = rec["duration_s"] = None
    else:
        rec["status"] = SET_EDITED
    return rec
