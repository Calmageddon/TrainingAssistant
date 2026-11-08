"""Websocket-Befehle für die Dashboard-Karte."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, SIGNAL_UPDATE
from .plan import PlanError

WS = f"{DOMAIN}/"


def async_setup_websocket(hass: HomeAssistant) -> None:
    for handler in (
        ws_subscribe,
        ws_history,
        ws_preview,
        ws_import_plan,
        ws_plan_source,
        ws_delete_plan,
        ws_edit_set,
        ws_delete_session,
        ws_set_next,
        ws_templates,
        ws_set_program,
        ws_import_template,
        ws_stats,
        ws_profile,
        ws_set_weekly_goal,
        ws_ha_users,
        ws_link_profile,
    ):
        websocket_api.async_register_command(hass, handler)


def _manager(hass: HomeAssistant):
    from . import get_manager  # noqa: PLC0415

    return get_manager(hass)


def _guard(connection: websocket_api.ActiveConnection, msg_id: int, func) -> Any:
    try:
        return True, func()
    except PlanError as err:
        connection.send_error(msg_id, "invalid_plan", "\n".join(err.errors))
    except (HomeAssistantError, KeyError, ValueError) as err:
        connection.send_error(msg_id, "failed", str(err))
    return False, None


@websocket_api.websocket_command({vol.Required("type"): WS + "subscribe"})
@callback
def ws_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Zustand sofort und bei jeder Änderung senden."""
    ok, manager = _guard(connection, msg["id"], lambda: _manager(hass))
    if not ok:
        return

    @callback
    def send() -> None:
        connection.send_message(websocket_api.event_message(msg["id"], manager.public_state()))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(hass, SIGNAL_UPDATE, send)
    connection.send_result(msg["id"])
    send()


@websocket_api.websocket_command({vol.Required("type"): WS + "history", vol.Optional("limit", default=30): int})
@callback
def ws_history(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass).history(msg["limit"]))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "preview", vol.Optional("plan_id"): str, vol.Optional("workout_id"): str}
)
@callback
def ws_preview(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(
        connection, msg["id"], lambda: _manager(hass).preview(msg.get("plan_id"), msg.get("workout_id"))
    )
    if ok:
        connection.send_result(msg["id"], {"steps": result})


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "import_plan", vol.Required("text"): str, vol.Optional("lang"): str}
)
@callback
def ws_import_plan(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass).import_plan(msg["text"], msg.get("lang")))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "plan_source", vol.Required("plan_id"): str})
@callback
def ws_plan_source(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass).plan_source(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"], {"text": result})


@websocket_api.websocket_command({vol.Required("type"): WS + "delete_plan", vol.Required("plan_id"): str})
@websocket_api.require_admin
@callback
def ws_delete_plan(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass).delete_plan(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS + "edit_set",
        vol.Optional("session_id"): vol.Any(None, str),
        vol.Required("set_id"): int,
        vol.Optional("reps"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(min=0))),
        vol.Optional("weight_kg"): vol.Any(None, vol.All(vol.Coerce(float), vol.Range(min=0))),
        vol.Optional("duration_s"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(min=0))),
        vol.Optional("skipped"): bool,
        vol.Optional("effort"): vol.Any(None, vol.In(["easy", "normal", "hard"])),
    }
)
@callback
def ws_edit_set(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    changes = {k: msg[k] for k in ("reps", "weight_kg", "duration_s", "skipped", "effort") if k in msg}
    ok, result = _guard(
        connection, msg["id"], lambda: _manager(hass).edit_set(msg.get("session_id"), msg["set_id"], changes)
    )
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "delete_session", vol.Required("session_id"): str})
@websocket_api.require_admin
@callback
def ws_delete_session(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass).delete_session(msg["session_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "set_next", vol.Required("plan_id"): str, vol.Required("workout_id"): str}
)
@callback
def ws_set_next(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass).set_next(msg["plan_id"], msg["workout_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "templates"})
@websocket_api.async_response
async def ws_templates(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        result = await _manager(hass).async_templates()
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], {"templates": result})


@websocket_api.websocket_command({vol.Required("type"): WS + "import_template", vol.Required("template_id"): str})
@websocket_api.async_response
async def ws_import_template(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        result = await _manager(hass).async_import_template(msg["template_id"])
    except PlanError as err:
        connection.send_error(msg["id"], "invalid_plan", "\n".join(err.errors))
        return
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "set_program", vol.Required("plan_id"): str})
@callback
def ws_set_program(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass).set_program(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "stats"})
@callback
def ws_stats(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Woche, Serie, Zeit, Muskelvolumen, Erholung, letzte Rekorde."""
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass).stats())
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS + "profile",
        vol.Required("action"): vol.In(["select", "add", "rename", "delete"]),
        vol.Optional("profile"): str,
        vol.Optional("name"): str,
    }
)
@callback
def ws_profile(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Personen: auswählen, anlegen, umbenennen, löschen."""
    m = _manager(hass)
    action = msg["action"]
    funcs = {
        "select": lambda: m.set_profile(msg["profile"]),
        "add": lambda: m.add_profile(msg.get("name", "")),
        "rename": lambda: m.rename_profile(msg["profile"], msg.get("name", "")),
        "delete": lambda: m.delete_profile(msg["profile"]),
    }
    ok, result = _guard(connection, msg["id"], funcs[action])
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "set_weekly_goal", vol.Required("goal"): vol.All(vol.Coerce(int), vol.Range(1, 14))}
)
@callback
def ws_set_weekly_goal(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass).set_weekly_goal(msg["goal"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "ha_users"})
@websocket_api.require_admin
@websocket_api.async_response
async def ws_ha_users(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """HA-Benutzer zum Verknüpfen mit Personen (nur für Administratoren)."""
    connection.send_result(msg["id"], {"users": await _manager(hass).async_ha_users()})


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "link_profile", vol.Required("profile"): str, vol.Optional("user_id"): vol.Any(None, str)}
)
@websocket_api.require_admin
@websocket_api.async_response
async def ws_link_profile(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        await _manager(hass).async_link_profile(msg["profile"], msg.get("user_id") or None)
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"])
