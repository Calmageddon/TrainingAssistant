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
        # RGB-Lampe als Lichtsignal (leer = Standard aus den Optionen bzw. Licht am Satelliten)
        vol.Optional("light"): vol.Any(None, "", cv.entity_id),
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
HISTORY_SCHEMA = vol.Schema({vol.Optional("limit", default=30): vol.All(vol.Coerce(int), vol.Range(min=1))})
EMPTY_SCHEMA = vol.Schema({})


def _person(schema: vol.Schema) -> vol.Schema:
    """Jede Aktion kann sagen, wessen Training gemeint ist (ID oder Name der Person)."""
    return schema.extend({vol.Optional("person"): vol.Any(None, "", cv.string)})


def async_setup_services(hass: HomeAssistant) -> None:
    from . import get_hub  # noqa: PLC0415 – Zirkelimport vermeiden

    def pick(call: ServiceCall, *, control: bool = True):
        """Trainer der gemeinten Person: Feld person → Satellit/Gerät → aufrufender Benutzer → einzige Person.
        Bedienen darf man nur das eigene Training (bzw. das einer Person ohne verknüpften Benutzer)."""
        hub = get_hub(hass)
        manager = hub.resolve(call.data.get("person") or None, user_id=call.context.user_id,
                              satellite=call.data.get("satellite") or None, device_id=call.data.get("device_id") or None)
        if control and not hub.can_control(manager.pid, call.context.user_id):
            raise error("not_your_workout")
        return manager

    def data(call: ServiceCall, *drop: str) -> dict[str, Any]:
        return {k: v for k, v in call.data.items() if k not in ("person", *drop)}

    async def start(call: ServiceCall) -> ServiceResponse:
        result = await pick(call).async_start(**data(call))
        return result if call.return_response else None

    async def next_(call: ServiceCall) -> None:
        await pick(call).async_next(**data(call))

    async def simple(call: ServiceCall) -> None:
        manager = pick(call)
        await {
            "undo": manager.async_undo,
            "skip": manager.async_skip,
            "pause": manager.async_pause,
            "finish": manager.async_finish,
        }[call.service]()

    async def abort(call: ServiceCall) -> None:
        await pick(call).async_abort(keep=call.data["keep"])

    async def import_plan(call: ServiceCall) -> ServiceResponse:
        # Pläne sind gemeinsam – egal über welche Person
        manager = next(iter(get_hub(hass).persons.values()))
        try:
            result = manager.import_plan(call.data["plan"])
        except PlanError as err:
            raise error("invalid_plan", errors="\n".join(err.errors)) from err
        return result if call.return_response else None

    async def delete_plan(call: ServiceCall) -> None:
        next(iter(get_hub(hass).persons.values())).delete_plan(call.data["plan_id"])

    async def set_next_workout(call: ServiceCall) -> None:
        pick(call).set_next(call.data["plan_id"], call.data["workout_id"])

    async def log_set(call: ServiceCall) -> None:
        await pick(call).async_log_set(**data(call))

    async def edit(call: ServiceCall) -> None:
        values: dict[str, Any] = data(call)
        session_id = values.pop("session_id", None)
        set_id = values.pop("set_id")
        pick(call).edit_set(session_id, set_id, values)

    async def history(call: ServiceCall) -> ServiceResponse:
        return pick(call, control=False).history(call.data["limit"])

    hass.services.async_register(DOMAIN, "start", start, _person(START_SCHEMA), supports_response=SupportsResponse.OPTIONAL)
    hass.services.async_register(DOMAIN, "next", next_, _person(NEXT_SCHEMA))
    for name in ("undo", "skip", "pause", "finish"):
        hass.services.async_register(DOMAIN, name, simple, _person(EMPTY_SCHEMA))
    hass.services.async_register(DOMAIN, "abort", abort, _person(ABORT_SCHEMA))

    async def adjust(call: ServiceCall) -> None:
        pick(call).async_adjust(call.data["field"], call.data["steps"])

    async def set_value(call: ServiceCall) -> None:
        pick(call).async_set_value(call.data["field"], call.data["value"])

    hass.services.async_register(DOMAIN, "adjust", adjust, _person(ADJUST_SCHEMA))
    hass.services.async_register(DOMAIN, "set_value", set_value, _person(SET_VALUE_SCHEMA))
    hass.services.async_register(
        DOMAIN, "import_plan", import_plan, IMPORT_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(DOMAIN, "delete_plan", delete_plan, PLAN_ID_SCHEMA)
    hass.services.async_register(DOMAIN, "set_next_workout", set_next_workout, _person(NEXT_WORKOUT_SCHEMA))

    async def set_program(call: ServiceCall) -> None:
        pick(call).set_program(call.data["plan_id"])

    hass.services.async_register(DOMAIN, "set_program", set_program, _person(PLAN_ID_SCHEMA))
    hass.services.async_register(DOMAIN, "log_set", log_set, _person(LOG_SET_SCHEMA))
    hass.services.async_register(DOMAIN, "edit_set", edit, _person(EDIT_SET_SCHEMA))
    hass.services.async_register(DOMAIN, "get_history", history, _person(HISTORY_SCHEMA),
                                 supports_response=SupportsResponse.ONLY)

    async def rest_adjust(call: ServiceCall) -> None:
        pick(call).async_rest_adjust(call.data["seconds"])

    async def get_stats(call: ServiceCall) -> ServiceResponse:
        return pick(call, control=False).stats()

    hass.services.async_register(DOMAIN, "rest_adjust", rest_adjust, _person(REST_SCHEMA))
    hass.services.async_register(DOMAIN, "get_stats", get_stats, _person(EMPTY_SCHEMA),
                                 supports_response=SupportsResponse.ONLY)
