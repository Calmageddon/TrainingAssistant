"""Übersetzbare Fehlermeldungen für Aktionen und Websocket-Befehle.

Die englischen Texte stehen hier (Rückfall), die Übersetzungen in strings.json /
translations/*.json unter "exceptions". HA zeigt sie in der Sprache des Nutzers an.
"""

from __future__ import annotations

from homeassistant.exceptions import ServiceValidationError

from .const import DOMAIN

MESSAGES: dict[str, str] = {
    "not_set_up": "TrainingAssistant is not set up",
    "template_not_found": "Template '{template}' does not exist",
    "plan_not_found": "Plan '{plan}' does not exist",
    "workout_not_found": "Workout '{workout}' does not exist in '{plan}'",
    "session_not_found": "Workout session '{session}' does not exist",
    "set_not_found": "Set {set} does not exist",
    "no_training": "No workout is running",
    "no_plan": "No training plan yet – please import a plan first",
    "already_running": "A workout is already running – finish or abort it first",
    "no_active_set": "There is no running set that can be adjusted",
    "no_weight": "This exercise has no weight",
    "no_sets_yet": "No set has been logged in this workout yet",
    "invalid_plan": "Plan is invalid:\n{errors}",
    "profile_not_found": "Person '{profile}' does not exist",
    "profile_busy": "Finish or abort the running workout before switching person",
    "profile_exists": "A person named '{profile}' already exists",
    "profile_name_missing": "Please enter a name",
    "profile_delete_active": "The active person cannot be deleted – switch to someone else first",
    "user_not_found": "This Home Assistant user does not exist",
}


def error(key: str, **placeholders: object) -> ServiceValidationError:
    """Fehler mit Übersetzungsschlüssel (englischer Text als Rückfall)."""
    ph = {k: str(v) for k, v in placeholders.items()}
    return ServiceValidationError(
        MESSAGES[key].format(**ph),
        translation_domain=DOMAIN,
        translation_key=key,
        translation_placeholders=ph,
    )
