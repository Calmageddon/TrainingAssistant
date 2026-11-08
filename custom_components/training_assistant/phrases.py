"""Gesprochene Texte (Ansagen, Rückfragen) in mehreren Sprachen.

Ohne Home-Assistant-Abhängigkeiten. Neue Sprache: PHRASES um einen Eintrag mit allen
Schlüsseln von "en" ergänzen (fehlende Schlüssel fallen auf Englisch zurück) und in
spoken.py die Zahlwörter/Antwortwörter ergänzen.
"""

from __future__ import annotations

from typing import Any

DEFAULT_LANG = "en"

PHRASES: dict[str, dict[str, str]] = {
    "en": {
        "weight": "{w} kilos",
        "seconds": "{s} seconds",
        "seconds_range": "{lo} to {hi} seconds",
        "hold_max": "hold as long as possible",
        "amrap": "as many reps as possible",
        "reps": "{n} reps",
        "per_side": " per side",
        "with_weight": "{t} with {w}",
        "tempo": ", tempo {tempo}",
        "round_of": "Round {r} of {n}",
        "round": "Round {r}",
        "set_of": "Set {s} of {n}",
        "set": "Set {s}",
        "and": " and ",
        "interval_rest": ", {s} seconds rest",
        "interval_block": "{name}: {rounds} rounds, {work} seconds of work{rest}. {exercises}. Press the button to start.",
        "circuit_rounds": "{n} rounds of",
        "circuit_cap": "{m} minutes, alternating:",
        "press_ready": "Press the button when you're ready.",
        "block_ready": "{name}: {how} {exercises}.{note} " + "{press}",
        "total_reps": "{n} reps in total, as many sets as needed",
        "total_reps_weight": ", with {w}",
        "sets_how": "{sets} sets, {target}",
        "exercise_ready": "{exercise}: {how}.{note} {press}",
        "q_duration": "{s} seconds as planned?",
        "q_hold": "How many seconds?",
        "q_amrap": "How many reps?",
        "q_weight": "{r} reps with {w} as planned?",
        "q_reps": "{r} reps as planned?",
        "time_up": "Time's up.",
        "total_reached": "{n} reps reached.",
        "intro": "Workout {w}.",
        "rest": "Rest {s} seconds.",
        "warmup": "Start with your warm-up and press the button when you're done.",
        "cooldown": "Finally, cool down. Press the button when you're done.",
        "next": "Next: {d}",
        "finished": "Workout complete. {n} sets logged. Great job.",
        "go": "Let's go. {d}",
        "hiit_done": "HIIT done.",
        "back": "Back. {d}",
        "block_skipped": "{name} skipped.",
        "skipped": "Skipped.",
        "paused": "Paused.",
        "resumed": "Let's continue.",
        "rest_over": "Rest is over. Go.",
        "time_cap_over": "Time's up. Finish the current exercise and press the button.",
        "interval_go": "Go: {exercise}.",
        "flow_go": "{exercise}.",
        "flow_done": "Flow complete.",
        "flow_block": "{name}: {count} steps, about {minutes} min. {exercises}. Press the button to start.",
        "side_left": "{name}, left side",
        "side_right": "{name}, right side",
        "block_flow": "Flow",
        "block_warmup": "Warm-up",
        "block_cooldown": "Cool-down",
        "block_sets": "Sets",
        "block_circuit": "Circuit",
        "block_interval": "HIIT",
        "decimal": ".",
        "record": "New record! {exercise}: {value}.",
        "record_weight": "{w}",
        "record_e1rm": "estimated max {w}",
        "record_reps": "{n} reps",
        "record_duration": "{s} seconds",
    },
    "de": {
        "weight": "{w} Kilo",
        "seconds": "{s} Sekunden",
        "seconds_range": "{lo} bis {hi} Sekunden",
        "hold_max": "so lange wie möglich halten",
        "amrap": "maximale Wiederholungen",
        "reps": "{n} Wiederholungen",
        "per_side": " pro Seite",
        "with_weight": "{t} mit {w}",
        "tempo": ", Tempo {tempo}",
        "round_of": "Runde {r} von {n}",
        "round": "Runde {r}",
        "set_of": "Satz {s} von {n}",
        "set": "Satz {s}",
        "and": " und ",
        "interval_rest": ", {s} Sekunden Pause",
        "interval_block": "{name}: {rounds} Runden, {work} Sekunden Arbeit{rest}. {exercises}. Drücken Sie den Knopf zum Starten.",
        "circuit_rounds": "{n} Runden mit",
        "circuit_cap": "{m} Minuten im Wechsel:",
        "press_ready": "Drücken Sie den Knopf, wenn Sie bereit sind.",
        "block_ready": "{name}: {how} {exercises}.{note} " + "{press}",
        "total_reps": "insgesamt {n} Wiederholungen, so viele Sätze wie nötig",
        "total_reps_weight": ", mit {w}",
        "sets_how": "{sets} Sätze, {target}",
        "exercise_ready": "{exercise}: {how}.{note} {press}",
        "q_duration": "{s} Sekunden wie geplant?",
        "q_hold": "Wie viele Sekunden?",
        "q_amrap": "Wie viele Wiederholungen?",
        "q_weight": "{r} mal {w} wie geplant?",
        "q_reps": "{r} Wiederholungen wie geplant?",
        "time_up": "Zeit um.",
        "total_reached": "{n} Wiederholungen erreicht.",
        "intro": "Training {w}.",
        "rest": "Pause {s} Sekunden.",
        "warmup": "Beginnen Sie mit dem Aufwärmen und drücken Sie den Knopf, wenn Sie fertig sind.",
        "cooldown": "Zum Abschluss: Cool Down. Drücken Sie den Knopf, wenn Sie fertig sind.",
        "next": "Als Nächstes: {d}",
        "finished": "Training beendet. {n} Sätze erfasst. Gute Arbeit.",
        "go": "Los geht's. {d}",
        "hiit_done": "HIIT geschafft.",
        "back": "Zurück. {d}",
        "block_skipped": "{name} übersprungen.",
        "skipped": "Übersprungen.",
        "paused": "Pause.",
        "resumed": "Weiter geht's.",
        "rest_over": "Pause vorbei. Los.",
        "time_cap_over": "Zeit um. Beenden Sie die laufende Übung und drücken Sie den Knopf.",
        "interval_go": "Los: {exercise}.",
        "flow_go": "{exercise}.",
        "flow_done": "Flow geschafft.",
        "flow_block": "{name}: {count} Abschnitte, etwa {minutes} min. {exercises}. Drücken Sie den Knopf zum Starten.",
        "side_left": "{name}, linke Seite",
        "side_right": "{name}, rechte Seite",
        "block_flow": "Flow",
        "block_warmup": "Aufwärmen",
        "block_cooldown": "Cool Down",
        "block_sets": "Sätze",
        "block_circuit": "Zirkel",
        "block_interval": "HIIT",
        "decimal": ",",
        "record": "Neuer Rekord! {exercise}: {value}.",
        "record_weight": "{w}",
        "record_e1rm": "geschätztes Maximum {w}",
        "record_reps": "{n} Wiederholungen",
        "record_duration": "{s} Sekunden",
    },
}


def normalize_lang(lang: str | None) -> str:
    """„de-DE“ → „de“; unbekannte Sprachen → Englisch."""
    base = (lang or DEFAULT_LANG).split("-")[0].split("_")[0].lower()
    return base if base in PHRASES else DEFAULT_LANG


class Speech:
    """Formuliert Ansagen in einer Sprache."""

    def __init__(self, lang: str | None) -> None:
        self.lang = normalize_lang(lang)
        self._p = PHRASES[self.lang]

    def t(self, key: str, **kw: Any) -> str:
        text = self._p.get(key) or PHRASES[DEFAULT_LANG][key]
        return text.format(**kw)

    # -- Bausteine -----------------------------------------------------------

    def number(self, value: float) -> str:
        if value == int(value):
            return str(int(value))
        return f"{value:g}".replace(".", self.t("decimal"))

    def weight(self, weight: float | None) -> str:
        return "" if weight is None else self.t("weight", w=self.number(weight))

    def block_name(self, step: dict) -> str:
        return step.get("block_name") or self.t(f"block_{step.get('block_type', 'sets')}")

    def target(self, step: dict) -> str:
        """„10 reps per side with 16 kilos, tempo 3-0-1“ / „30 to 45 seconds“."""
        if step.get("duration_range"):
            lo, hi = step["duration_range"]
            text = self.t("seconds_range", lo=lo, hi=hi)
        elif step.get("target_duration"):
            text = self.t("seconds", s=step["target_duration"])
        elif step.get("hold_max"):
            text = self.t("hold_max")
        elif step.get("amrap"):
            text = self.t("amrap")
        else:
            reps = step.get("target_reps")
            text = self.t("reps", n=reps) if reps else ""
        if text and step.get("per_side"):
            text += self.t("per_side")
        if step.get("target_weight") is not None:
            w = self.weight(step["target_weight"])
            text = self.t("with_weight", t=text, w=w) if text else w
        if step.get("tempo"):
            text += self.t("tempo", tempo=step["tempo"])
        return text

    def position(self, step: dict) -> str:
        if step.get("round"):
            if step.get("rounds"):
                return self.t("round_of", r=step["round"], n=step["rounds"])
            return self.t("round", r=step["round"])
        if step.get("set_no"):
            if step.get("sets"):
                return self.t("set_of", s=step["set_no"], n=step["sets"])
            return self.t("set", s=step["set_no"])
        return ""

    def describe_step(self, step: dict) -> str:
        """„Round 2 of 3. Goblet Squats, 10 reps with 16 kilos.“"""
        main = f"{step['exercise_name']}, {self.target(step)}".rstrip(", ")
        parts = [p for p in (self.position(step), main) if p]
        return ". ".join(parts) + "."

    def describe_block(self, steps: list[dict], idx: int) -> str:
        step = steps[idx]
        btype = step["block_type"]
        name = self.block_name(step)
        if btype == "flow":
            minutes = max(1, round(step.get("total_s", 0) / 60))
            return self.t("flow_block", name=name, count=len(step.get("segments", [])), minutes=minutes,
                          exercises=", ".join(dict.fromkeys(step["exercise_names"])))
        if btype == "interval":
            rest = self.t("interval_rest", s=step["rest_s"]) if step["rest_s"] else ""
            return self.t("interval_block", name=name, rounds=step["rounds"], work=step["work_s"], rest=rest,
                          exercises=self.t("and").join(step["exercise_names"]))
        note = f" {step['block_note']}" if step.get("block_note") else ""
        end = step.get("block_end") or {}
        press = self.t("press_ready")
        if btype == "circuit":
            names: list[str] = []
            for s in steps[idx:]:
                if s["block"] != step["block"] or s.get("round") != 1:
                    break
                names.append(s["exercise_name"])
            if step.get("rounds"):
                how = self.t("circuit_rounds", n=step["rounds"])
            else:
                how = self.t("circuit_cap", m=self.number(end.get("time_cap_s", 0) / 60))
            return self.t("block_ready", name=name, how=how, exercises=", ".join(names), note=note, press=press)
        if end.get("total_reps"):
            how = self.t("total_reps", n=end["total_reps"])
            if step.get("target_weight") is not None:
                how += self.t("total_reps_weight", w=self.weight(step["target_weight"]))
        else:
            how = self.t("sets_how", sets=step["sets"], target=self.target(step))
        return self.t("exercise_ready", exercise=step["exercise_name"], how=how, note=note, press=press)

    def record(self, exercise: str, found: dict) -> str:
        """„New record! Goblet Squat: 18 kilos.“"""
        kind, value = found["kind"], found["value"]
        if kind in ("weight", "e1rm"):
            text = self.t(f"record_{kind}", w=self.weight(value))
        elif kind == "reps":
            text = self.t("record_reps", n=self.number(value))
        else:
            text = self.t("record_duration", s=self.number(value))
        return self.t("record", exercise=exercise, value=text)

    def segment_name(self, seg: dict) -> str:
        """Name eines Zeitabschnitts, bei Seiten mit „linke/rechte Seite“."""
        if seg.get("side") in ("left", "right"):
            return self.t(f"side_{seg['side']}", name=seg["name"])
        return seg["name"]

    def question(self, set_rec: dict) -> str | None:
        """Rückfrage nach einem Satz. None, wenn nichts zu fragen ist."""
        if set_rec.get("target_duration"):
            return self.t("q_duration", s=set_rec["target_duration"])
        if set_rec.get("hold_max"):
            return self.t("q_hold")
        if set_rec.get("amrap"):
            return self.t("q_amrap")
        if set_rec.get("target_reps") is None:
            return None
        if set_rec.get("target_weight") is not None:
            return self.t("q_weight", r=set_rec["target_reps"], w=self.weight(set_rec["target_weight"]))
        return self.t("q_reps", r=set_rec["target_reps"])
