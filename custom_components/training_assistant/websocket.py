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
        ws_exercise_library,
        ws_save_plan,
        ws_delete_plan,
        ws_edit_set,
        ws_delete_session,
        ws_set_next,
        ws_templates,
        ws_template_preview,
        ws_set_program,
        ws_import_template,
        ws_stats,
        ws_session_summary,
        ws_profile,
        ws_set_weekly_goal,
        ws_ha_users,
        ws_link_profile,
    ):
        websocket_api.async_register_command(hass, handler)


def _hub(hass: HomeAssistant):
    from . import get_hub  # noqa: PLC0415

    return get_hub(hass)


def _manager(hass: HomeAssistant, connection: websocket_api.ActiveConnection | None = None, msg: dict | None = None):
    """Trainer der Person, die die Karte gerade anzeigt (Feld person), sonst die des angemeldeten Benutzers,
    sonst die erste Person. Nur lesen – zum Bedienen _control()."""
    hub = _hub(hass)
    key = (msg or {}).get("person")
    if key:
        return hub.manager(key)
    user = connection.user.id if connection and connection.user else None
    pid = hub.person_of_user(user)
    return hub.persons[pid] if pid else next(iter(hub.persons.values()))


def _control(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict):
    """Wie _manager, aber zum Bedienen: nur das eigene Training bzw. das einer Person ohne verknüpften Benutzer."""
    from .errors import error  # noqa: PLC0415

    manager = _manager(hass, connection, msg)
    if not _hub(hass).can_control(manager.pid, connection.user.id if connection.user else None):
        raise error("not_your_workout")
    return manager


def _guard(connection: websocket_api.ActiveConnection, msg_id: int, func) -> Any:
    try:
        return True, func()
    except PlanError as err:
        connection.send_error(msg_id, "invalid_plan", "\n".join(err.errors))
    except (HomeAssistantError, KeyError, ValueError) as err:
        connection.send_error(msg_id, "failed", str(err))
    return False, None


@websocket_api.websocket_command({vol.Required("type"): WS + "subscribe", vol.Optional("person"): vol.Any(None, str)})
@callback
def ws_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Zustand sofort und bei jeder Änderung senden."""
    ok, manager = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg))
    if not ok:
        return
    hub = _hub(hass)
    user_id = connection.user.id if connection.user else None

    @callback
    def send() -> None:
        if hub.persons.get(manager.pid) is not manager:
            return  # Person gelöscht – die Karte wechselt zu einer anderen
        # can_control: darf dieser Benutzer das Training bedienen (sonst nur zuschauen)
        state = {**manager.public_state(), "can_control": hub.can_control(manager.pid, user_id),
                 "my_profile": hub.person_of_user(user_id)}
        connection.send_message(websocket_api.event_message(msg["id"], state))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(hass, SIGNAL_UPDATE, send)
    connection.send_result(msg["id"])
    send()


@websocket_api.websocket_command({vol.Required("type"): WS + "history", vol.Optional("person"): vol.Any(None, str), vol.Optional("limit", default=30): int})
@callback
def ws_history(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).history(msg["limit"]))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "preview", vol.Optional("person"): vol.Any(None, str), vol.Optional("plan_id"): str, vol.Optional("workout_id"): str}
)
@callback
def ws_preview(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(
        connection, msg["id"], lambda: _manager(hass, connection, msg).preview(msg.get("plan_id"), msg.get("workout_id"))
    )
    if ok:
        connection.send_result(msg["id"], {"steps": result})


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "import_plan", vol.Optional("person"): vol.Any(None, str), vol.Required("text"): str, vol.Optional("lang"): str}
)
@callback
def ws_import_plan(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).import_plan(msg["text"], msg.get("lang")))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "plan_source", vol.Optional("person"): vol.Any(None, str), vol.Required("plan_id"): str})
@callback
def ws_plan_source(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).plan_source(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "exercise_library", vol.Optional("person"): vol.Any(None, str)})
@websocket_api.async_response
async def ws_exercise_library(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Übungsauswahl im Editor: alle bekannten Übungen und die Kategorien für eigene Pläne."""
    try:
        result = await _manager(hass, connection, msg).async_exercise_library()
    except (HomeAssistantError, KeyError, ValueError) as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS + "save_plan", vol.Optional("person"): vol.Any(None, str),
        vol.Required("plan"): dict,
        vol.Optional("plan_id"): vol.Any(None, str),
        vol.Optional("category"): vol.Any(None, str),
        vol.Optional("lang"): str,
    }
)
@callback
def ws_save_plan(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Plan aus dem Editor speichern (neu oder geändert); ungültig → Fehler „invalid_plan“ mit allen Meldungen."""
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).save_plan(
        msg["plan"], msg.get("plan_id"), msg.get("category"), msg.get("lang")))
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "delete_plan", vol.Optional("person"): vol.Any(None, str), vol.Required("plan_id"): str})
@websocket_api.require_admin
@callback
def ws_delete_plan(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).delete_plan(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS + "edit_set", vol.Optional("person"): vol.Any(None, str),
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
        connection, msg["id"], lambda: _control(hass, connection, msg).edit_set(msg.get("session_id"), msg["set_id"], changes)
    )
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "delete_session", vol.Optional("person"): vol.Any(None, str), vol.Required("session_id"): str})
@websocket_api.require_admin
@callback
def ws_delete_session(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _control(hass, connection, msg).delete_session(msg["session_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "set_next", vol.Optional("person"): vol.Any(None, str), vol.Required("plan_id"): str, vol.Required("workout_id"): str}
)
@callback
def ws_set_next(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _control(hass, connection, msg).set_next(msg["plan_id"], msg["workout_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "templates", vol.Optional("person"): vol.Any(None, str)})
@websocket_api.async_response
async def ws_templates(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        result = await _manager(hass, connection, msg).async_templates()
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], {"templates": result})


@websocket_api.websocket_command({vol.Required("type"): WS + "import_template", vol.Optional("person"): vol.Any(None, str), vol.Required("template_id"): str})
@websocket_api.async_response
async def ws_import_template(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        result = await _manager(hass, connection, msg).async_import_template(msg["template_id"])
    except PlanError as err:
        connection.send_error(msg["id"], "invalid_plan", "\n".join(err.errors))
        return
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "template_preview", vol.Optional("person"): vol.Any(None, str), vol.Required("template_id"): str})
@websocket_api.async_response
async def ws_template_preview(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Workouts und Übungen einer Vorlage anzeigen, ohne sie zu übernehmen."""
    try:
        result = await _manager(hass, connection, msg).async_template_preview(msg["template_id"])
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "set_program", vol.Optional("person"): vol.Any(None, str), vol.Required("plan_id"): str})
@callback
def ws_set_program(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _control(hass, connection, msg).set_program(msg["plan_id"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "stats", vol.Optional("person"): vol.Any(None, str)})
@callback
def ws_stats(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Woche, Serie, Zeit, Muskelvolumen, Erholung, letzte Rekorde."""
    ok, result = _guard(connection, msg["id"], lambda: _manager(hass, connection, msg).stats())
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command({vol.Required("type"): WS + "session_summary", vol.Optional("person"): vol.Any(None, str), vol.Optional("session_id"): str})
@websocket_api.async_response
async def ws_session_summary(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Zusammenfassung eines gespeicherten Trainings (Abschluss-Ansicht der Karte). Wartet aufs Speichern."""
    try:
        result = await _manager(hass, connection, msg).async_session_summary(msg.get("session_id"))
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"], {"summary": result})


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS + "profile", vol.Optional("person"): vol.Any(None, str),
        vol.Required("action"): vol.In(["select", "add", "rename", "delete", "figure", "devices"]),
        vol.Optional("profile"): str,
        vol.Optional("name"): str,
        vol.Optional("figure"): str,
        vol.Optional("satellite"): vol.Any(None, str),
        vol.Optional("light"): vol.Any(None, str),
        vol.Optional("notify"): vol.Any(None, str),
    }
)
@callback
def ws_profile(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Personen: anlegen, umbenennen, löschen, Figur, Geräte (Satellit, Lampe, Handy-Hinweis).

    „select“ ändert nichts mehr: Jede Person trainiert für sich, die Karte wählt nur, wen sie anzeigt.
    Ändern darf man die eigene Person bzw. eine ohne verknüpften Benutzer (Admins alle).
    """
    from .errors import error  # noqa: PLC0415

    hub = _hub(hass)
    action = msg["action"]
    user = connection.user
    if action in ("rename", "delete", "figure", "devices"):
        try:
            pid = hub.find_profile(msg.get("profile", ""))
        except HomeAssistantError as err:
            connection.send_error(msg["id"], "failed", str(err))
            return
        if not (user and user.is_admin) and not hub.can_control(pid, user.id if user else None):
            connection.send_error(msg["id"], "failed", str(error("not_your_workout")))
            return
    if action == "select":
        connection.send_result(msg["id"])
        return
    if action in ("add", "delete"):
        async def run() -> None:
            try:
                result = await (hub.async_add_profile(msg.get("name", "")) if action == "add"
                                else hub.async_delete_profile(msg["profile"]))
            except HomeAssistantError as err:
                connection.send_error(msg["id"], "failed", str(err))
                return
            connection.send_result(msg["id"], result)

        hass.async_create_task(run())
        return
    funcs = {
        "rename": lambda: hub.rename_profile(msg["profile"], msg.get("name", "")),
        "figure": lambda: hub.set_profile_figure(msg["profile"], msg.get("figure", "")),
        "devices": lambda: hub.set_profile_devices(msg["profile"], {k: msg[k] for k in ("satellite", "light", "notify")
                                                                     if k in msg}),
    }
    ok, result = _guard(connection, msg["id"], funcs[action])
    if ok:
        connection.send_result(msg["id"], result)


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "set_weekly_goal", vol.Optional("person"): vol.Any(None, str), vol.Required("goal"): vol.All(vol.Coerce(int), vol.Range(1, 14))}
)
@callback
def ws_set_weekly_goal(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    ok, _ = _guard(connection, msg["id"], lambda: _control(hass, connection, msg).set_weekly_goal(msg["goal"]))
    if ok:
        connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): WS + "ha_users", vol.Optional("person"): vol.Any(None, str)})
@websocket_api.require_admin
@websocket_api.async_response
async def ws_ha_users(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """HA-Benutzer zum Verknüpfen mit Personen (nur für Administratoren)."""
    connection.send_result(msg["id"], {"users": await _hub(hass).async_ha_users()})


@websocket_api.websocket_command(
    {vol.Required("type"): WS + "link_profile", vol.Optional("person"): vol.Any(None, str), vol.Required("profile"): str, vol.Optional("user_id"): vol.Any(None, str)}
)
@websocket_api.require_admin
@websocket_api.async_response
async def ws_link_profile(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    try:
        await _hub(hass).async_link_profile(msg["profile"], msg.get("user_id") or None)
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "failed", str(err))
        return
    connection.send_result(msg["id"])
