"""Aktionen (Services) von TrainingAssistant."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv

from .errors import error
from .const import DOMAIN
from .plan import PlanError

START_SCHEMA = vol.Schema(
    {
        vol.Optional("plan_id"): cv.string,
        vol.Optional("workout_id"): cv.string,
        # Leer erlaubt: Sprachbefehl aus der App/Tastatur hat kein Gerät → Standard-Satellit bzw. stumm
        vol.Optional("satellite"): vol.Any(None, "", cv.entity_id),
        vol.Optional("device_id"): vol.Any(None, cv.string),
        vol.Optional("speak_intro", default=True): cv.boolean,
    }
)
NEXT_SCHEMA = vol.Schema(
    {
        vol.Optional("reps"): vol.All(vol.Coerce(int), vol.Range(min=0)),
        vol.Optional("weight_kg"): vol.All(vol.Coerce(float), vol.Range(min=0)),
        vol.Optional("duration_s"): vol.All(vol.Coerce(int), vol.Range(min=0)),
        vol.Optional("effort"): vol.Any(None, vol.In(["easy", "normal", "hard"])),
    }
)
ADJUST_SCHEMA = vol.Schema(
    {vol.Required("field"): vol.In(["reps", "weight"]), vol.Optional("steps", default=1): vol.Coerce(int)}
)
SET_VALUE_SCHEMA = vol.Schema(
    {vol.Required("field"): vol.In(["reps", "weight"]), vol.Required("value"): vol.All(vol.Coerce(float), vol.Range(min=0))}
)
IMPORT_SCHEMA = vol.Schema({vol.Required("plan"): cv.string})
PLAN_ID_SCHEMA = vol.Schema({vol.Required("plan_id"): cv.string})
NEXT_WORKOUT_SCHEMA = vol.Schema({vol.Required("plan_id"): cv.string, vol.Required("workout_id"): cv.string})
ABORT_SCHEMA = vol.Schema({vol.Optional("keep", default=True): cv.boolean})
LOG_SET_SCHEMA = vol.Schema(
    {
        vol.Optional("text"): cv.string,
        vol.Optional("reps"): vol.All(vol.Coerce(int), vol.Range(min=0)),
        vol.Optional("weight_kg"): vol.All(vol.Coerce(float), vol.Range(min=0)),
        vol.Optional("duration_s"): vol.All(vol.Coerce(int), vol.Range(min=0)),
        vol.Optional("effort"): vol.Any(None, vol.In(["easy", "normal", "hard"])),
    }
)
EDIT_SET_SCHEMA = vol.Schema(
    {
        vol.Optional("session_id"): cv.string,
        vol.Required("set_id"): vol.Coerce(int),
        vol.Optional("reps"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(min=0))),
        vol.Optional("weight_kg"): vol.Any(None, vol.All(vol.Coerce(float), vol.Range(min=0))),
        vol.Optional("duration_s"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(min=0))),
        vol.Optional("skipped", default=False): cv.boolean,
        vol.Optional("effort"): vol.Any(None, vol.In(["easy", "normal", "hard"])),
    }
)
REST_SCHEMA = vol.Schema({vol.Optional("seconds", default=15): vol.Coerce(int)})
PROFILE_SCHEMA = vol.Schema({vol.Required("profile"): cv.string})
HISTORY_SCHEMA = vol.Schema({vol.Optional("limit", default=30): vol.All(vol.Coerce(int), vol.Range(min=1))})


def async_setup_services(hass: HomeAssistant) -> None:
    from . import get_manager  # noqa: PLC0415 – Zirkelimport vermeiden

    async def start(call: ServiceCall) -> ServiceResponse:
        result = await get_manager(hass).async_start(**call.data)
        return result if call.return_response else None

    async def next_(call: ServiceCall) -> None:
        await get_manager(hass).async_next(**call.data)

    async def simple(call: ServiceCall) -> None:
        manager = get_manager(hass)
        await {
            "undo": manager.async_undo,
            "skip": manager.async_skip,
            "pause": manager.async_pause,
            "finish": manager.async_finish,
        }[call.service]()

    async def abort(call: ServiceCall) -> None:
        await get_manager(hass).async_abort(keep=call.data["keep"])

    async def import_plan(call: ServiceCall) -> ServiceResponse:
        try:
            result = get_manager(hass).import_plan(call.data["plan"])
        except PlanError as err:
            raise error("invalid_plan", errors="\n".join(err.errors)) from err
        return result if call.return_response else None

    async def delete_plan(call: ServiceCall) -> None:
        get_manager(hass).delete_plan(call.data["plan_id"])

    async def set_next_workout(call: ServiceCall) -> None:
        get_manager(hass).set_next(call.data["plan_id"], call.data["workout_id"])

    async def log_set(call: ServiceCall) -> None:
        await get_manager(hass).async_log_set(**call.data)

    async def edit(call: ServiceCall) -> None:
        data: dict[str, Any] = dict(call.data)
        session_id = data.pop("session_id", None)
        set_id = data.pop("set_id")
        get_manager(hass).edit_set(session_id, set_id, data)

    async def history(call: ServiceCall) -> ServiceResponse:
        return get_manager(hass).history(call.data["limit"])

    hass.services.async_register(DOMAIN, "start", start, START_SCHEMA, supports_response=SupportsResponse.OPTIONAL)
    hass.services.async_register(DOMAIN, "next", next_, NEXT_SCHEMA)
    for name in ("undo", "skip", "pause", "finish"):
        hass.services.async_register(DOMAIN, name, simple)
    hass.services.async_register(DOMAIN, "abort", abort, ABORT_SCHEMA)

    async def adjust(call: ServiceCall) -> None:
        get_manager(hass).async_adjust(call.data["field"], call.data["steps"])

    async def set_value(call: ServiceCall) -> None:
        get_manager(hass).async_set_value(call.data["field"], call.data["value"])

    hass.services.async_register(DOMAIN, "adjust", adjust, ADJUST_SCHEMA)
    hass.services.async_register(DOMAIN, "set_value", set_value, SET_VALUE_SCHEMA)
    hass.services.async_register(
        DOMAIN, "import_plan", import_plan, IMPORT_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(DOMAIN, "delete_plan", delete_plan, PLAN_ID_SCHEMA)
    hass.services.async_register(DOMAIN, "set_next_workout", set_next_workout, NEXT_WORKOUT_SCHEMA)

    async def set_program(call: ServiceCall) -> None:
        get_manager(hass).set_program(call.data["plan_id"])

    hass.services.async_register(DOMAIN, "set_program", set_program, PLAN_ID_SCHEMA)
    hass.services.async_register(DOMAIN, "log_set", log_set, LOG_SET_SCHEMA)
    hass.services.async_register(DOMAIN, "edit_set", edit, EDIT_SET_SCHEMA)
    hass.services.async_register(DOMAIN, "get_history", history, HISTORY_SCHEMA,
                                 supports_response=SupportsResponse.ONLY)

    async def rest_adjust(call: ServiceCall) -> None:
        get_manager(hass).async_rest_adjust(call.data["seconds"])

    async def set_profile(call: ServiceCall) -> None:
        get_manager(hass).set_profile(call.data["profile"])

    async def get_stats(call: ServiceCall) -> ServiceResponse:
        return get_manager(hass).stats()

    hass.services.async_register(DOMAIN, "rest_adjust", rest_adjust, REST_SCHEMA)
    hass.services.async_register(DOMAIN, "set_profile", set_profile, PROFILE_SCHEMA)
    hass.services.async_register(DOMAIN, "get_stats", get_stats, supports_response=SupportsResponse.ONLY)
