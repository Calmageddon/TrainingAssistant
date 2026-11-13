"""Regelbasierte Vorschläge für das nächste Training (progressive overload).

Ohne Home-Assistant-Abhängigkeiten.

Regeln:
- double: Erst Wiederholungen steigern (pro Training +1 auf den schwächsten Satz),
  bis alle Sätze das obere Ende des Bereichs erreichen. Dann +increment_kg und
  zurück auf das untere Ende.
- linear: Alle Sätze mit den Ziel-Wiederholungen geschafft → +increment_kg,
  sonst Gewicht halten.
- reps: Für Übungen ohne (oder mit festem) Gewicht. Alle Sätze mit dem letzten Ziel
  geschafft → nächstes Mal +increment Wiederholungen, bis max_reps (bzw. dem oberen
  Ende eines Bereichs). Danach Hinweis auf eine schwerere Variante.
- none: Werte wie zuletzt.

Anstrengung (effort im Satz, „leicht“/„schwer“ per Sprache oder Karte):
- War ein Satz schwer, wird nicht gesteigert (gleiche Vorgabe nochmal).
- Waren alle Sätze leicht, wird doppelt gesteigert (+2 Wdh. bzw. +2× increment).

Sätze nach Zeit (suggest_duration): alle Zeiten geschafft → +TIME_STEP_S Sekunden, alle leicht → doppelt,
schwer → halten. Ohne Obergrenze – auch über das Ende eines Zeitbereichs im Plan hinaus.
"""

from __future__ import annotations

from typing import Any

SKIPPED = "skipped"
# Schritt der Zeit-Progression (Sekunden)
TIME_STEP_S = 5


def _round(value: float) -> float:
    value = round(value, 2)
    return int(value) if value == int(value) else value


def done_sets(sets: list[dict]) -> list[dict]:
    """Sätze, die für die Progression zählen (nicht übersprungen, mit Wiederholungen)."""
    return [s for s in sets if s.get("status") != SKIPPED and isinstance(s.get("reps"), (int, float))]


def suggest(
    last_sets: list[dict],
    *,
    rep_range: tuple[int, int] | None,
    progression: dict[str, Any],
    plan_weight: float | None,
) -> dict[str, Any]:
    """Zielwerte für die nächste Session.

    Rückgabe: {"weight_kg", "reps", "reason", "increased"}
    """
    lo, hi = rep_range if rep_range else (None, None)
    last = done_sets(last_sets)
    if rep_range is None:
        # Zeit-Sätze und reps: max – keine Progression, Gewicht wie zuletzt
        weights = [s["weight_kg"] for s in last if s.get("weight_kg") is not None]
        return {
            "weight_kg": min(weights) if weights else plan_weight,
            "reps": None,
            "reason": "Ohne Progression (Zeit oder max.)", "reason_key": "no_progression_timed", "reason_params": {},
            "increased": False,
        }
    if not last:
        return {"weight_kg": plan_weight, "reps": lo, "reason": "Planwerte (noch kein Verlauf)", "reason_key": "plan_values", "reason_params": {}, "increased": False}

    weights = [s["weight_kg"] for s in last if s.get("weight_kg") is not None]
    # Vorsichtig: das kleinste Gewicht der letzten Session ist die Basis
    base = min(weights) if weights else plan_weight
    reps_done = [int(s["reps"]) for s in last]
    ptype = progression.get("type", "none")
    inc = progression.get("increment_kg", 0)
    efforts = [s.get("effort") for s in last]
    hard = "hard" in efforts
    easy = bool(efforts) and all(e == "easy" for e in efforts)

    def hold(reps: int | None) -> dict[str, Any]:
        return {"weight_kg": base, "reps": reps, "reason": "Zuletzt schwer → gleiche Vorgabe nochmal",
                "reason_key": "hard_hold", "reason_params": {}, "increased": False}

    if ptype == "double":
        if all(r >= hi for r in reps_done):
            if hard and base is not None:
                return hold(hi)
            if base is None:
                return {
                    "weight_kg": None,
                    "reps": hi,
                    "reason": f"Alle Sätze mit {hi} Wdh. geschafft – schwerere Variante oder Zusatzgewicht",
                    "reason_key": "harder_variant", "reason_params": {"reps": hi},
                    "increased": False,
                }
            return {
                "weight_kg": _round(base + inc),
                "reps": lo,
                "reason": f"Alle Sätze mit {hi} Wdh. geschafft → +{_round(inc)} kg",
                "reason_key": "all_reps_add_weight", "reason_params": {"reps": hi, "kg": _round(inc)},
                "increased": True,
            }
        if hard:
            return hold(max(lo, min(hi, min(reps_done))))
        target = max(lo, min(hi, min(reps_done) + (2 if easy else 1)))
        if easy:
            return {"weight_kg": base, "reps": target, "reason": f"Leicht → Ziel {target} Wdh. (bis {hi})",
                    "reason_key": "easy_target", "reason_params": {"target": target, "max": hi}, "increased": True}
        return {
            "weight_kg": base,
            "reps": target,
            "reason": (f"Gewicht halten, Ziel {target} Wdh. (bis {hi})" if base is not None
                       else f"Ziel {target} Wdh. (bis {hi})"),
            "reason_key": "hold_weight_target" if base is not None else "target_reps",
            "reason_params": {"target": target, "max": hi},
            "increased": False,
        }

    if ptype == "reps":
        step = int(progression.get("increment", 1))
        cap = progression.get("max_reps") or (hi if hi != lo else None)
        # Ziel der letzten Session (im Satz gespeichert), sonst Planwert
        targets = [int(s["target_reps"]) for s in last if isinstance(s.get("target_reps"), (int, float))]
        last_target = max(targets) if targets else lo
        if all(r >= last_target for r in reps_done):
            if cap is not None and last_target >= cap:
                return {
                    "weight_kg": base,
                    "reps": cap,
                    "reason": f"Obergrenze von {cap} Wdh. erreicht – schwerere Variante oder Zusatzgewicht",
                    "reason_key": "cap_reached", "reason_params": {"cap": cap},
                    "increased": False,
                }
            if hard:
                return hold(last_target)
            step = step * 2 if easy else step
            target = last_target + step if cap is None else min(cap, last_target + step)
            if easy:
                return {"weight_kg": base, "reps": target,
                        "reason": f"Alle Sätze leicht → +{target - last_target} Wdh.",
                        "reason_key": "easy_add_reps", "reason_params": {"add": target - last_target},
                        "increased": True}
            return {
                "weight_kg": base,
                "reps": target,
                "reason": f"Alle Sätze mit {last_target} Wdh. geschafft → +{target - last_target} Wdh.",
                "reason_key": "all_reps_add_reps", "reason_params": {"reps": last_target, "add": target - last_target},
                "increased": True,
            }
        return {
            "weight_kg": base,
            "reps": last_target,
            "reason": f"Ziel {last_target} Wdh. noch nicht in allen Sätzen geschafft – nochmal",
            "reason_key": "repeat_target", "reason_params": {"target": last_target},
            "increased": False,
        }

    if ptype == "linear":
        if all(r >= lo for r in reps_done):
            if base is None:
                return {"weight_kg": None, "reps": lo, "reason": "Alle Sätze geschafft", "reason_key": "all_done", "reason_params": {},
                        "increased": False}
            if hard:
                return hold(lo)
            if easy:
                return {"weight_kg": _round(base + 2 * inc), "reps": lo,
                        "reason": f"Alle Sätze leicht → +{_round(2 * inc)} kg",
                        "reason_key": "easy_add_weight", "reason_params": {"kg": _round(2 * inc)}, "increased": True}
            return {
                "weight_kg": _round(base + inc),
                "reps": lo,
                "reason": f"Alle Sätze geschafft → +{_round(inc)} kg",
                "reason_key": "all_done_add_weight", "reason_params": {"kg": _round(inc)},
                "increased": True,
            }
        return {
            "weight_kg": base,
            "reps": lo,
            "reason": "Nicht alle Sätze geschafft → Gewicht halten", "reason_key": "not_all_hold", "reason_params": {},
            "increased": False,
        }

    return {"weight_kg": base, "reps": lo, "reason": "Feste Vorgabe aus dem Plan (ohne Progression)", "reason_key": "fixed", "reason_params": {},
            "increased": False}


def suggest_duration(
    last_sets: list[dict],
    *,
    plan_duration: int,
    plan_weight: float | None,
    fixed: bool = False,
) -> dict[str, Any]:
    """Vorschlag für einen Satz nach Zeit (gleiche Regeln wie Hero Upgrade `suggestDuration`).

    Gezählt werden nur Sätze nach Zeit aus Satz-Blöcken (mit set_no), nicht HIIT-/Flow-Abschnitte.
    fixed = Progression am Eintrag ausdrücklich abgeschaltet. Rückgabe wie suggest() plus "duration_s".
    """
    done = [s for s in last_sets if s.get("status") != SKIPPED and isinstance(s.get("duration_s"), (int, float))
            and s.get("set_no") is not None]
    weights = [s["weight_kg"] for s in done if s.get("weight_kg") is not None]
    weight = min(weights) if weights else plan_weight

    def r(duration: int, key: str, reason: str, params: dict | None = None, increased: bool = False) -> dict[str, Any]:
        return {"weight_kg": weight, "reps": None, "duration_s": duration, "reason": reason, "reason_key": key,
                "reason_params": params or {}, "increased": increased}

    if fixed:
        return r(plan_duration, "fixed", "Feste Vorgabe aus dem Plan (ohne Progression)")
    if not done:
        return r(plan_duration, "plan_values", "Planwerte (noch kein Verlauf)")
    targets = [s["target_duration"] if isinstance(s.get("target_duration"), (int, float)) else s["duration_s"] for s in done]
    target = int(max([plan_duration, *targets]))
    efforts = [s.get("effort") for s in done]
    if not all(s["duration_s"] >= (s["target_duration"] if isinstance(s.get("target_duration"), (int, float)) else target)
               for s in done):
        return r(target, "time_repeat", f"{target} s noch nicht in jedem Satz geschafft – nochmal", {"target": target})
    if "hard" in efforts:
        return r(target, "hard_hold", "Zuletzt schwer → gleiche Vorgabe nochmal")
    easy = all(e == "easy" for e in efforts)
    add = 2 * TIME_STEP_S if easy else TIME_STEP_S
    key = "time_easy_add" if easy else "time_add"
    reason = f"{'Alles leicht' if easy else 'Alle Zeiten geschafft'} → +{add} s ({target + add} s)"
    return r(target + add, key, reason, {"add": add, "target": target + add}, True)
