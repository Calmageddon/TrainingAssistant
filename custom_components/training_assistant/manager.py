"""Verbindet die Ablauf-Engine mit Home Assistant.

Aufgaben: Pläne und Verlauf speichern (helpers.storage), Effekte der Engine
ausführen (Ansagen, Rückfragen, Pausen- und HIIT-Timer, Events) und Entitäten
sowie die Dashboard-Karte über Änderungen informieren.
"""

from __future__ import annotations

import asyncio
from collections import ChainMap
import copy
from datetime import timedelta
import logging
import re
import time
from typing import Any
from pathlib import Path
import uuid

import voluptuous as vol
import yaml

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .errors import error
from .const import (
    CONF_ANNOUNCE,
    CONF_ASK_AFTER_SET,
    CONF_DEFAULT_SATELLITE,
    CONF_DEFAULT_LIGHT,
    PLAN_SCHEMA_VERSION,
    CONF_SATELLITE_LIGHT,
    CONF_NOTIFY,
    CHART_POINTS,
    DEFAULT_WEEKLY_GOAL,
    CONF_QUESTION_TIMEOUT,
    CONF_VOICE_LANGUAGE,
    DEFAULT_QUESTION_TIMEOUT,
    DOMAIN,
    EVENT_NAME,
    HOLD_COUNTDOWN_S,
    PHASE_ACTIVE,
    PHASE_INTERVAL,
    PHASE_READY,
    SET_CONFIRMED,
    SET_CORRECTED,
    SET_EDITED,
    SET_PENDING,
    SET_PLANNED,
    SET_SKIPPED,
    SET_UNCONFIRMED,
    SIGNAL_PERSON_ADDED,
    SIGNAL_PERSON_REMOVED,
    SIGNAL_UPDATE,
    STORAGE_KEY,
    STORAGE_VERSION,
)
from .engine import Effects, Engine, edit_set, new_session
from .plan import (
    DEFAULT_BLOCK_NAMES,
    SIDE_SWITCH_S,
    PlanError,
    build_steps,
    find_workout,
    parse_plan_text,
    rep_bounds,
    slugify,
)
from .images import DEFAULT_FIGURE, FIGURES, Catalog, Pictos, map_pictos, map_plan
from . import glow
from .phrases import Speech, normalize_lang
from .progression import suggest
from .spoken import parse_answer
from . import stats as st

_LOGGER = logging.getLogger(__name__)

SAT_DOMAIN = "assist_satellite"
# Frühere Standardnamen, die beim Laden ersetzt werden
RENAMED_DEFAULTS = {"Abwärmen"}
# Übungen, die eine eigene Kennung bekommen haben: (Planname der Vorlage, alt, neu). Gleich wie Hero Upgrade
# (RENAMED_EXERCISES). Gilt nur für Pläne dieser Vorlage – z. B. bleibt kb_swing in anderen Plänen beidarmig.
RENAMED_EXERCISES = [
    ("Kettlebell Swing & Get-up", "kb_swing", "kb_swing_one_arm"),  # einarmiger Swing ≠ beidarmiger Swing
]
# Daten, die jeder Person gehören (Speicher: data["persons"][pid]). Pläne und die Personenliste sind gemeinsam.
# Jede Person hat ihren eigenen TrainingManager – mehrere Personen können gleichzeitig trainieren.
PERSON_KEYS = ("sessions", "program", "rotation", "next", "active", "last_session_id")


def _fresh_person(pid: str) -> dict[str, Any]:
    return {"profile": pid, "sessions": [], "program": None, "rotation": {}, "next": None, "active": None,
            "last_session_id": None}
# Sätze, die als „gemacht“ für Rekorde zählen
RECORD_STATUSES = {SET_PLANNED, SET_CONFIRMED, SET_CORRECTED, SET_EDITED}


def _now() -> str:
    return dt_util.utcnow().isoformat()


class TrainingHub:
    """Zentrale pro Config-Entry: Speicher, gemeinsame Pläne, Personen – und ein TrainingManager je Person.

    Speicher: {"plans": {...}, "profiles": {pid: {...}}, "persons": {pid: {sessions, program, rotation, next, active,
    last_session_id, profile}}}. Jede Person trainiert unabhängig (eigene Timer, Sprache, Licht).
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._store: Store[dict[str, Any]] = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.root: dict[str, Any] = {"plans": {}, "profiles": {}, "persons": {}}
        self.persons: dict[str, TrainingManager] = {}
        self.catalog: Catalog | None = None
        self.pictos: Pictos | None = None

    # -- Laden / Speichern ------------------------------------------------

    async def async_load(self) -> None:
        stored = await self._store.async_load()
        root = self.root
        if stored:
            root.update(stored)
        self.catalog = await self.hass.async_add_executor_job(Catalog.load)
        self.pictos = await self.hass.async_add_executor_job(Pictos.load)
        if not root.get("profiles"):
            # Vor den Profilen: der bisherige Verlauf wird das erste Profil (Name des Besitzers)
            owner = await self.hass.auth.async_get_owner()
            name = owner.name if owner and owner.name else "Me"
            root["profiles"] = {"p1": {"id": "p1", "name": name, "weekly_goal": DEFAULT_WEEKLY_GOAL}}
            root.setdefault("profile", "p1")
        persons = root.setdefault("persons", {})
        if "profile_data" in root or any(k in root for k in PERSON_KEYS):
            # Altes Format (eine aktive Person direkt im Speicher, die anderen in profile_data) → je Person ein Bereich
            current = root.pop("profile", None) or next(iter(root["profiles"]))
            persons[current] = {k: root.pop(k, None) for k in PERSON_KEYS}
            for pid, pdata in (root.pop("profile_data", None) or {}).items():
                persons[pid] = {k: (pdata or {}).get(k) for k in PERSON_KEYS}
        root.pop("profile", None)
        root.pop("profile_data", None)
        for pid in root["profiles"]:
            pdata = persons.setdefault(pid, _fresh_person(pid))
            for key, value in _fresh_person(pid).items():
                if pdata.get(key) is None:
                    pdata[key] = value
            pdata["profile"] = pid
            if "program" not in pdata and pdata.get("next"):
                pdata["program"] = pdata["next"]["plan_id"]
        for pid in list(persons):
            if pid not in root["profiles"]:
                persons.pop(pid)
        for stored_plan in root["plans"].values():
            if "images" not in stored_plan:  # Pläne von vor der Bildfunktion
                stored_plan["images"] = map_plan(stored_plan["data"], self.catalog)
            # Bilder bei jedem Start neu zuordnen: So bekommen auch alte Pläne neue Bilder
            stored_plan["pictos"] = map_pictos(stored_plan["data"], self.pictos, stored_plan["images"])
        self._rename_exercises()
        for pid in root["profiles"]:
            await self._add_manager(pid)

    async def _add_manager(self, pid: str) -> TrainingManager:
        manager = TrainingManager(self, pid)
        self.persons[pid] = manager
        await manager.async_load()
        return manager

    async def async_unload(self) -> None:
        for manager in self.persons.values():
            await manager.async_unload()
        await self._store.async_save(self.root)

    @callback
    def save(self) -> None:
        self._store.async_delay_save(lambda: self.root, 1)

    def save_now(self) -> asyncio.Task:
        """Sofort speichern (Ende eines Trainings – die Zusammenfassung wartet darauf)."""
        return self.hass.async_create_task(self._store.async_save(self.root))

    @callback
    def changed(self) -> None:
        """Gemeinsames hat sich geändert (Pläne, Personen): speichern, alle Personen aktualisieren."""
        for manager in self.persons.values():
            manager._groups_cache.clear()
            manager._sync_next()
        self.save()
        async_dispatcher_send(self.hass, SIGNAL_UPDATE)

    def _rename_exercises(self) -> None:
        """RENAMED_EXERCISES anwenden – bei jedem Laden, ändert nur, was noch die alte Kennung trägt.

        Plan (Übungsliste, Blöcke, Quelltext, Bildzuordnung), Verlauf aller Personen und laufende Trainings.
        """
        d = self.root
        persons = list(d["persons"].values())
        for plan_name, old, new in RENAMED_EXERCISES:
            plan_id = slugify(plan_name)

            def fix(items: list | None) -> None:
                for x in items or []:
                    if isinstance(x, dict) and x.get("exercise") == old:
                        x["exercise"] = new

            stored = d["plans"].get(plan_id)
            if stored and old in stored["data"].get("exercises", {}) and new not in stored["data"]["exercises"]:
                exercises = stored["data"]["exercises"]
                stored["data"]["exercises"] = {(new if k == old else k): v for k, v in exercises.items()}
                for workout in stored["data"].get("workouts", []):
                    for block in workout.get("blocks", []):
                        fix([block])
                        exs = block.get("exercises")
                        if isinstance(exs, list):
                            block["exercises"] = [new if e == old else e for e in exs]
                            fix(block["exercises"])
                if stored.get("source"):
                    stored["source"] = re.sub(rf"\b{re.escape(old)}\b", new, stored["source"])
                if old in (stored.get("images") or {}):
                    stored["images"][new] = stored["images"].pop(old)
            for person in persons:
                for sess in person.get("sessions") or []:
                    if sess.get("plan_id") == plan_id:
                        fix(sess.get("sets"))
                active = person.get("active")
                if not active or active.get("plan_id") != plan_id:
                    continue
                fix(active.get("sets"))
                fix(active.get("steps"))
                for step in active.get("steps") or []:
                    if isinstance(step.get("exercises"), list):
                        step["exercises"] = [new if e == old else e for e in step["exercises"]]

    # -- Personen ---------------------------------------------------------

    def find_profile(self, key: str) -> str:
        """Person über ID oder Namen (ohne Groß-/Kleinschreibung)."""
        profiles = self.root["profiles"]
        if key in profiles:
            return key
        for pid, prof in profiles.items():
            if prof["name"].casefold() == str(key).strip().casefold():
                return pid
        raise error("profile_not_found", profile=key)

    def manager(self, key: str) -> TrainingManager:
        return self.persons[self.find_profile(key)]

    def person_of_user(self, user_id: str | None) -> str | None:
        """Person, die mit diesem HA-Benutzer verknüpft ist."""
        if not user_id:
            return None
        return next((pid for pid, p in self.root["profiles"].items() if p.get("user_id") == user_id), None)

    def person_of_satellite(self, satellite: str | None, device_id: str | None = None) -> str | None:
        """Person, der dieser Satellit gehört (Einstellung der Person)."""
        sats = {satellite} if satellite else set()
        if device_id:
            registry = er.async_get(self.hass)
            sats |= {e.entity_id for e in er.async_entries_for_device(registry, device_id) if e.domain == SAT_DOMAIN}
        if not sats:
            return None
        return next((pid for pid, p in self.root["profiles"].items() if p.get("satellite") in sats), None)

    def resolve(self, person: str | None = None, *, user_id: str | None = None, satellite: str | None = None,
                device_id: str | None = None) -> TrainingManager:
        """Wessen Training? Angabe → Satellit/Gerät → angemeldeter Benutzer → einzige Person → Fehler."""
        if person:
            return self.manager(person)
        pid = self.person_of_satellite(satellite, device_id) or self.person_of_user(user_id)
        if pid:
            return self.persons[pid]
        if len(self.persons) == 1:
            return next(iter(self.persons.values()))
        raise error("person_required")

    def can_control(self, pid: str, user_id: str | None) -> bool:
        """Bedienen darf man das eigene Training und das von Personen ohne verknüpften Benutzer (z. B. Tablet)."""
        owner = self.root["profiles"][pid].get("user_id")
        return not owner or owner == user_id or user_id is None

    async def async_add_profile(self, name: str) -> dict[str, Any]:
        name = name.strip()
        if not name:
            raise error("profile_name_missing")
        profiles = self.root["profiles"]
        if any(p["name"].casefold() == name.casefold() for p in profiles.values()):
            raise error("profile_exists", profile=name)
        base = slugify(name) or "p"
        pid, n = base, 2
        while pid in profiles:
            pid, n = f"{base}_{n}", n + 1
        goal = next(iter(profiles.values()), {}).get("weekly_goal", DEFAULT_WEEKLY_GOAL)
        prof = {"id": pid, "name": name, "weekly_goal": goal}
        profiles[pid] = prof
        self.root["persons"][pid] = _fresh_person(pid)
        await self._add_manager(pid)
        async_dispatcher_send(self.hass, SIGNAL_PERSON_ADDED, pid)
        self.changed()
        return prof

    def rename_profile(self, key: str, name: str) -> None:
        pid = self.find_profile(key)
        name = name.strip()
        if not name:
            raise error("profile_name_missing")
        if any(p["name"].casefold() == name.casefold() and i != pid for i, p in self.root["profiles"].items()):
            raise error("profile_exists", profile=name)
        self.root["profiles"][pid]["name"] = name
        self.changed()

    def set_profile_figure(self, key: str, figure: str) -> None:
        """Figur auf den Übungsbildern (m = männlich, w = weiblich)."""
        pid = self.find_profile(key)
        if figure not in FIGURES:
            raise error("figure_invalid", figure=figure)
        self.root["profiles"][pid]["figure"] = figure
        self.changed()

    def set_profile_devices(self, key: str, changes: dict[str, Any]) -> None:
        """Satellit, Lampe und Handy-Hinweis einer Person (leer = Standard aus den Optionen)."""
        pid = self.find_profile(key)
        prof = self.root["profiles"][pid]
        for field in ("satellite", "light", "notify"):
            if field in changes:
                if changes[field]:
                    prof[field] = changes[field]
                else:
                    prof.pop(field, None)
        self.changed()

    async def async_delete_profile(self, key: str) -> None:
        """Person samt Verlauf löschen – nicht während ihres Trainings, nicht die letzte Person."""
        pid = self.find_profile(key)
        if len(self.root["profiles"]) <= 1:
            raise error("profile_delete_active")
        manager = self.persons[pid]
        if manager.active:
            raise error("profile_busy")
        await manager.async_unload()
        self.persons.pop(pid)
        self.root["profiles"].pop(pid)
        self.root["persons"].pop(pid, None)
        async_dispatcher_send(self.hass, SIGNAL_PERSON_REMOVED, pid)
        self.changed()

    async def async_ha_users(self) -> list[dict[str, str]]:
        """Echte Home-Assistant-Benutzer (ohne System-Benutzer) zum Verknüpfen."""
        users = await self.hass.auth.async_get_users()
        return sorted(({"id": u.id, "name": u.name or u.id} for u in users
                       if u.is_active and not u.system_generated), key=lambda u: u["name"].lower())

    async def async_link_profile(self, key: str, user_id: str | None) -> None:
        """Person mit einem HA-Benutzer verknüpfen (None = lösen). Ein Benutzer gehört zu höchstens einer Person."""
        pid = self.find_profile(key)
        if user_id:
            if await self.hass.auth.async_get_user(user_id) is None:
                raise error("user_not_found")
            for prof in self.root["profiles"].values():
                if prof.get("user_id") == user_id:
                    prof.pop("user_id")
            self.root["profiles"][pid]["user_id"] = user_id
        else:
            self.root["profiles"][pid].pop("user_id", None)
        self.changed()


class TrainingManager:
    """Training einer Person. Sieht ihre eigenen Daten und die gemeinsamen (Pläne, Personen) als eine Tabelle."""

    def __init__(self, hub: TrainingHub, pid: str) -> None:
        self.hub = hub
        self.hass = hub.hass
        self.entry = hub.entry
        self.pid = pid
        # Lesen: erst die Daten der Person, dann die gemeinsamen. Schreiben auf oberster Ebene: Daten der Person.
        self.data: ChainMap = ChainMap(hub.root["persons"][pid], hub.root)
        self._voice_queue: asyncio.Queue[tuple] = asyncio.Queue()
        self._voice_task: asyncio.Task | None = None
        self._ask_cancel: asyncio.Event | None = None
        self._interval_task: asyncio.Task | None = None
        self._rest_unsub: CALLBACK_TYPE | None = None
        self._block_unsub: CALLBACK_TYPE | None = None
        self._hold_unsub: CALLBACK_TYPE | None = None
        # Lichtsignal: Lampe der laufenden Session, zuletzt gesetzter Zustand, Timer bis „rot“ und für Aufleuchten
        self._light: dict[str, Any] | None = None
        self._light_state: str | None = None
        self._light_unsub: CALLBACK_TYPE | None = None
        self._light_flash_unsub: CALLBACK_TYPE | None = None
        self._light_hold_until = 0.0  # bis dahin bleibt das goldene Rekord-Leuchten stehen (time.monotonic)
        # Speichern direkt nach dem Ende eines Trainings – die Zusammenfassung wartet darauf
        self._saving: asyncio.Task | None = None
        self._groups_cache: dict[tuple[str | None, str], list[str]] = {}

    # ------------------------------------------------------------------
    # Laden / Speichern
    # ------------------------------------------------------------------

    @property
    def _catalog(self) -> Catalog | None:
        return self.hub.catalog

    @property
    def _pictos(self) -> Pictos | None:
        return self.hub.pictos

    async def async_load(self) -> None:
        """Daten der Person vorbereiten (nach dem Laden des Speichers bzw. beim Anlegen)."""
        self._sync_next()
        if self.data.get("active"):
            self._attach_images(self.data["active"]["steps"], self.data["active"]["plan_id"])
        active = self.data.get("active")
        if active:
            # Umbenannte Standardnamen in bereits gestarteten Trainings nachziehen
            for step in active["steps"]:
                if step.get("block_type") == "cooldown" and step.get("block_name") in RENAMED_DEFAULTS:
                    step["block_name"] = DEFAULT_BLOCK_NAMES["cooldown"]
            # Nach einem Neustart: laufende Timer/Rückfragen sind weg
            if active["phase"] == PHASE_INTERVAL:
                active["phase"] = PHASE_READY
            active["interval"] = None
            active["hold"] = None  # Satz nach Zeit: nach dem Neustart wieder mit dem Countdown beginnen
            active["rest_until"] = None
            active.pop("rest_remaining", None)
            # Zeitlimit eines Blocks überlebt keinen Neustart: als abgelaufen werten
            if active.pop("block_until", None) or active.pop("block_remaining", None):
                active["block_expired"] = True
            pending = active.get("pending_question")
            if pending is not None:
                for rec in active["sets"]:
                    if rec["id"] == pending and rec["status"] == SET_PENDING:
                        rec["status"] = SET_UNCONFIRMED
                active["pending_question"] = None
        self._voice_task = self.entry.async_create_background_task(
            self.hass, self._voice_worker(), f"{DOMAIN}_voice_{self.pid}"
        )
        if active:
            self._sync_hold()

    async def async_unload(self) -> None:
        self._cancel_light_timers()
        self._cancel_hold()
        self._cancel_rest()
        self._cancel_block_timer()
        self._stop_interval()
        if self._voice_task:
            self._voice_task.cancel()
        # Lampe nach dem Entladen wie vor dem Training
        if self._light:
            await self._apply_light(self._light, "off")

    @callback
    def _changed(self) -> None:
        self.hub.save()
        async_dispatcher_send(self.hass, SIGNAL_UPDATE)
        self._sync_light()

    # ------------------------------------------------------------------
    # Pläne
    # ------------------------------------------------------------------

    def import_plan(self, text: str, lang: str | None = None, *, template: str | None = None,
                    category: str | None = None, plan_id: str | None = None) -> dict[str, Any]:
        """Plan aus YAML/JSON-Text importieren. Gleicher Name = Plan wird ersetzt.

        lang: Sprache der Prüfmeldungen (Standard: Sprache von Home Assistant).
        template: ID der Vorlage, aus der der Plan stammt (im Editor nur als Kopie bearbeitbar).
        category: Kategorie für „Meine Pläne“ (Standard: bisherige, sonst Gruppe der Vorlage, sonst „other“).
        plan_id: vorhandenen Plan ersetzen (Editor), sonst aus dem Namen.
        """
        plan = parse_plan_text(text, lang or self.hass.config.language)
        self._groups_cache.clear()
        plan_id = plan_id or slugify(plan["name"])
        old = self.data["plans"].get(plan_id) or {}
        images = map_plan(plan, self._catalog) if self._catalog else {}
        pictos = map_pictos(plan, self._pictos, images) if self._pictos else {}
        self.data["plans"][plan_id] = {
            "id": plan_id,
            "name": plan["name"],
            "source": text,
            "data": plan,
            "images": images,
            "pictos": pictos,
            "imported_at": old.get("imported_at") if old and not template else _now(),
            **({"template": template} if template else {}),
            **({"category": category or old.get("category")} if (category or old.get("category")) else {}),
            **({"edited_at": _now()} if old and not template else {}),
        }
        if self.data.get("program") not in self.data["plans"]:
            self.data["program"] = plan_id
        self._sync_next()
        self._changed()
        self.hub.changed()  # andere Personen ohne Programm bekommen den neuen Plan
        missing = [plan["exercises"][k]["name"] for k, v in pictos.items() if not v]
        return {
            "plan_id": plan_id,
            "name": plan["name"],
            "workouts": [w["id"] for w in plan["workouts"]],
            "images": {"matched": len(pictos) - len(missing), "total": len(pictos), "missing": missing},
        }

    # -- Mitgelieferte Vorlagen -------------------------------------------

    TEMPLATE_DIR = Path(__file__).parent / "templates"
    # Reihenfolge = Anzeige-Reihenfolge: (Titel, Symbol, wofür / was man braucht)
    # Titel/Beschreibung hier nur als Rückfall – die Karte übersetzt sie über group_key (tg.<key>)
    TEMPLATE_GROUPS = {
        "kraft": ("Strength & hypertrophy", "mdi:weight-lifter",
                  "Barbell, dumbbells, machines – muscle and maximal strength in the gym or home gym."),
        "bodyweight": ("Bodyweight – no equipment", "mdi:home-heart",
                       "At home, in a hotel, on the road – circuits and strength with a chair and sofa."),
        "calisthenics": ("Calisthenics", "mdi:human-handsup",
                         "Pull-up bar and dip bars – progress through ever harder variations up to skills."),
        "kettlebell": ("Kettlebell", "mdi:kettlebell",
                       "One or two bells – strength, muscular endurance and conditioning in little time."),
        "hiit": ("HIIT & Tabata", "mdi:timer-outline",
                 "Short, hard intervals – timed, with beeps or announcements. Bodyweight, kettlebell, bike, rower or running."),
        "ausdauer": ("Endurance", "mdi:run",
                     "Running and steady cardio – step by step to more stamina. Timed, runs on its own."),
        "yoga": ("Yoga & mobility", "mdi:yoga",
                 "Flows, stretching and balance – runs on its own, every pose is announced. A mat is enough."),
    }

    def _read_templates(self) -> list[dict[str, Any]]:
        out = []
        for path in sorted(self.TEMPLATE_DIR.glob("*.yaml")):
            text = path.read_text(encoding="utf-8")
            try:
                plan = parse_plan_text(text)
            except PlanError as err:
                _LOGGER.error("Vorlage %s ist ungültig: %s", path.name, err)
                continue
            group = path.stem.split("-", 1)[0]
            title, icon, about = self.TEMPLATE_GROUPS.get(group, ("More", "mdi:dumbbell", ""))
            out.append({
                "id": path.stem,
                "group": title,
                "group_key": group if group in self.TEMPLATE_GROUPS else "other",
                "group_icon": icon,
                "group_about": about,
                "name": plan["name"],
                "description": plan.get("description"),
                "workouts": [w["name"] for w in plan["workouts"]],
                "text": text,
                "_order": list(self.TEMPLATE_GROUPS).index(group) if group in self.TEMPLATE_GROUPS else 99,
            })
        out.sort(key=lambda t: t.pop("_order"))  # stabil: innerhalb der Gruppe nach Dateiname
        return out

    async def async_templates(self) -> list[dict[str, Any]]:
        """Mitgelieferte Vorlagen (ohne Text), mit Hinweis, ob schon importiert."""
        templates = await self.hass.async_add_executor_job(self._read_templates)
        installed = {p["name"] for p in self.data["plans"].values()}
        return [{k: v for k, v in t.items() if k != "text"} | {"installed": t["name"] in installed}
                for t in templates]

    async def async_import_template(self, template_id: str) -> dict[str, Any]:
        templates = await self.hass.async_add_executor_job(self._read_templates)
        template = next((t for t in templates if t["id"] == template_id), None)
        if template is None:
            raise error("template_not_found", template=template_id)
        return self.import_plan(template["text"], template=template_id)

    async def async_template_preview(self, template_id: str) -> dict[str, Any]:
        """Vorschau einer Vorlage, ohne sie zu importieren: alle Workouts mit Schritten (Planwerte, ohne Verlauf)."""
        templates = await self.hass.async_add_executor_job(self._read_templates)
        template = next((t for t in templates if t["id"] == template_id), None)
        if template is None:
            raise error("template_not_found", template=template_id)
        plan = parse_plan_text(template["text"])
        images = map_plan(plan, self._catalog) if self._catalog else {}
        pictos = map_pictos(plan, self._pictos, images) if self._pictos else {}
        workouts = []
        for w in plan["workouts"]:
            steps = build_steps(plan, w["id"])
            for step in steps:
                if step.get("exercise"):
                    step["image"] = pictos.get(step["exercise"])
                elif step.get("type") == "interval":
                    step["images"] = [pictos.get(e) for e in step.get("exercises", [])]
            workouts.append({"id": w["id"], "name": w["name"], "description": w.get("description"), "steps": steps})
        return {"id": template_id, "name": plan["name"], "description": plan.get("description"), "workouts": workouts}

    def delete_plan(self, plan_id: str) -> None:
        self._groups_cache.clear()
        if self.data["plans"].pop(plan_id, None) is None:
            raise error("plan_not_found", plan=plan_id)
        for person in self.hub.root["persons"].values():
            (person.get("rotation") or {}).pop(plan_id, None)
        self._changed()
        self.hub.changed()  # alle Personen: nächstes Workout neu bestimmen

    # -- Aktives Programm und Reihenfolge ----------------------------------
    #  program  = Plan, in dem man sich bewegt
    #  rotation = pro Plan das als Nächstes fällige Workout (Position bleibt beim Wechseln erhalten)
    #  next     = abgeleitet: {plan_id, workout_id} des aktiven Programms

    def _sync_next(self) -> None:
        plans = self.data["plans"]
        rotation = self.data.setdefault("rotation", {})
        program = self.data.get("program")
        if program not in plans:
            program = next(iter(plans), None)
            self.data["program"] = program
        if program is None:
            self.data["next"] = None
            return
        ids = [w["id"] for w in plans[program]["data"]["workouts"]]
        if rotation.get(program) not in ids:
            rotation[program] = ids[0]
        self.data["next"] = {"plan_id": program, "workout_id": rotation[program]}

    def set_program(self, plan_id: str) -> None:
        """Programm wechseln – es geht dort weiter, wo man zuletzt war."""
        self._plan(plan_id)
        self.data["program"] = plan_id
        self._sync_next()
        self._changed()

    def program_workouts(self) -> list[dict[str, Any]]:
        """Workouts des aktiven Programms mit Position (für Auswahl und Karte)."""
        nxt = self.data.get("next")
        if not nxt:
            return []
        workouts = self.data["plans"][nxt["plan_id"]]["data"]["workouts"]
        return [
            {"workout_id": w["id"], "label": f"{w['name']} ({i}/{len(workouts)})", "name": w["name"],
             "position": i, "count": len(workouts)}
            for i, w in enumerate(workouts, 1)
        ]

    def workout_options(self) -> list[dict[str, str]]:
        """Alle Workouts aller Pläne (für Auswahl-Entität und Karte)."""
        return [
            {
                "plan_id": p["id"],
                "workout_id": w["id"],
                "label": f"{p['name']} · {w['name']}",
            }
            for p in self.data["plans"].values()
            for w in p["data"]["workouts"]
        ]

    def set_next(self, plan_id: str, workout_id: str) -> None:
        plan = self._plan(plan_id)
        try:
            find_workout(plan, workout_id)
        except KeyError as err:
            raise error("workout_not_found", workout=workout_id, plan=plan_id) from err
        self.data["program"] = plan_id
        self.data.setdefault("rotation", {})[plan_id] = workout_id
        self._sync_next()
        self._changed()

    def _plan(self, plan_id: str) -> dict:
        try:
            return self.data["plans"][plan_id]["data"]
        except KeyError as err:
            raise error("plan_not_found", plan=plan_id) from err

    def _advance_rotation(self, plan_id: str, workout_id: str) -> None:
        stored = self.data["plans"].get(plan_id)
        if not stored:
            return
        ids = [w["id"] for w in stored["data"]["workouts"]]
        if workout_id in ids:
            # nur die Position dieses Plans rückt weiter – das aktive Programm bleibt, wie es ist
            self.data.setdefault("rotation", {})[plan_id] = ids[(ids.index(workout_id) + 1) % len(ids)]
        self._sync_next()

    # ------------------------------------------------------------------
    # Verlauf und Vorschläge
    # ------------------------------------------------------------------

    def last_sets(self, exercise_id: str, plan_id: str | None = None, workout_id: str | None = None) -> list[dict]:
        """Gültige Sätze der letzten Session mit dieser Übung (mit Wiederholungen oder Zeit – die Zeit-Progression
        braucht die Sätze nach Zeit; die Wdh.-Progression filtert selbst).

        Mit plan_id/workout_id zuerst aus demselben Workout (gleiche Vorgaben, z. B. 6–8 statt 10 Wdh.),
        nur wenn es dort noch keinen Verlauf gibt aus irgendeinem.
        """
        if workout_id is not None:
            for sess in reversed(self.data["sessions"]):
                if sess["plan_id"] != plan_id or sess["workout_id"] != workout_id:
                    continue
                sets = [
                    x for x in sess["sets"]
                    if x["exercise"] == exercise_id and x["status"] != SET_SKIPPED
                    and (x.get("reps") is not None or x.get("duration_s") is not None)
                ]
                if sets:
                    return sets
        for sess in reversed(self.data["sessions"]):
            sets = [
                x for x in sess["sets"]
                if x["exercise"] == exercise_id and x["status"] != SET_SKIPPED
                and (x.get("reps") is not None or x.get("duration_s") is not None)
            ]
            if sets:
                return sets
        return []

    def last_done_sets(self, exercise_id: str) -> list[dict]:
        """Wie last_sets, aber auch Zeit-Sätze (für die Anzeige „Zuletzt“)."""
        for sess in reversed(self.data["sessions"]):
            sets = [
                x for x in sess["sets"]
                if x["exercise"] == exercise_id and x["status"] != SET_SKIPPED
                and (x.get("reps") is not None or x.get("duration_s") is not None)
            ]
            if sets:
                return sets
        return []

    def preview(self, plan_id: str | None = None, workout_id: str | None = None) -> list[dict]:
        plan_id, workout_id = self._resolve_workout(plan_id, workout_id)
        steps = build_steps(self._plan(plan_id), workout_id, lambda ex: self.last_sets(ex, plan_id, workout_id))
        self._attach_images(steps, plan_id)
        return steps

    def _exercise_context(self, exercise_id: str) -> tuple[Any, dict, Any] | None:
        """(rep_range, progression, plan_weight) des ersten Vorkommens in den Plänen."""
        plans = list(self.data["plans"].values())
        nxt = self.data.get("next")
        plans.sort(key=lambda p: 0 if nxt and p["id"] == nxt["plan_id"] else 1)
        for stored in plans:
            plan = stored["data"]
            def_prog = plan.get("defaults", {}).get("progression", {"type": "none"})
            for w in plan["workouts"]:
                for block in w["blocks"]:
                    items = [block] if block["type"] == "sets" else block.get("exercises", []) \
                        if block["type"] == "circuit" else []
                    for item in items:
                        if item.get("exercise") == exercise_id:
                            return (rep_bounds(item.get("reps")), item.get("progression") or def_prog,
                                    item.get("weight_kg"))
        return None

    def history(self, limit: int = 30) -> dict[str, Any]:
        sessions = list(reversed(self.data["sessions"]))[:limit]
        exercises: dict[str, dict[str, Any]] = {}
        for sess in self.data["sessions"]:
            for rec in sess["sets"]:
                if rec["status"] == SET_SKIPPED or rec.get("reps") is None and rec.get("duration_s") is None:
                    continue
                ex = exercises.setdefault(
                    rec["exercise"],
                    {"exercise": rec["exercise"], "name": rec["exercise_name"], "sessions": 0, "best_weight": None,
                     "last_date": None, "_last_session": None, "points": []},
                )
                if ex["_last_session"] != sess["id"]:
                    ex["sessions"] += 1
                    ex["_last_session"] = sess["id"]
                    ex["last_date"] = sess["started_at"]
                    ex["points"].append({"date": sess["started_at"], "weight_kg": rec.get("weight_kg"),
                                         "reps": rec.get("reps"), "duration_s": rec.get("duration_s")})
                else:
                    # pro Training jeweils der beste Wert
                    pt = ex["points"][-1]
                    for key in ("weight_kg", "reps", "duration_s"):
                        if (rec.get(key) or 0) > (pt[key] or 0):
                            pt[key] = rec.get(key)
                w = rec.get("weight_kg")
                if w is not None and (ex["best_weight"] is None or w > ex["best_weight"]):
                    ex["best_weight"] = w
        for ex_id, ex in exercises.items():
            ex.pop("_last_session")
            last = self.last_sets(ex_id)
            ex["last_sets"] = [
                {"reps": x.get("reps"), "weight_kg": x.get("weight_kg"), "duration_s": x.get("duration_s"),
                 "per_side": x.get("per_side", False)}
                for x in self.last_done_sets(ex_id)
            ]
            ctx = self._exercise_context(ex_id)
            if ctx:
                ex["suggestion"] = suggest(last, rep_range=ctx[0], progression=ctx[1], plan_weight=ctx[2])
            else:
                ex["suggestion"] = None
            ex["points"] = ex["points"][-CHART_POINTS:]
            ex["image"] = self.image_for(ex_id)
            ex["bests"] = st.bests([x for sess in self.data["sessions"] for x in sess["sets"] if x["exercise"] == ex_id])
        return {
            "sessions": sessions,
            "exercises": sorted(exercises.values(), key=lambda e: e["name"].lower()),
        }

    def delete_session(self, session_id: str) -> None:
        before = len(self.data["sessions"])
        self.data["sessions"] = [s for s in self.data["sessions"] if s["id"] != session_id]
        if len(self.data["sessions"]) == before:
            raise error("session_not_found", session=session_id)
        self._changed()

    def edit_set(self, session_id: str | None, set_id: int, changes: dict[str, Any]) -> dict:
        active = self.data.get("active")
        if active and (session_id is None or session_id == active["id"]):
            sets = active["sets"]
            if active.get("pending_question") == set_id:
                active["pending_question"] = None
                if self._ask_cancel:
                    self._ask_cancel.set()
        else:
            sess = next((s for s in self.data["sessions"] if s["id"] == session_id), None)
            if sess is None:
                raise error("session_not_found", session=session_id)
            sets = sess["sets"]
        try:
            rec = edit_set(sets, set_id, changes)
        except KeyError as err:
            raise error("set_not_found", set=set_id) from err
        if active and sets is active["sets"]:
            effects = Engine(active).check_block_end()
            if effects:
                self.hass.async_create_task(self._run(effects))
        self._changed()
        return rec

    # ------------------------------------------------------------------
    # Session steuern
    # ------------------------------------------------------------------

    @property
    def voice_lang(self) -> str:
        """Sprache für Ansagen/Antworten: Einstellung, sonst Sprache von Home Assistant."""
        chosen = self.entry.options.get(CONF_VOICE_LANGUAGE, "auto")
        return normalize_lang(self.hass.config.language if chosen in (None, "", "auto") else chosen)

    @property
    def active(self) -> dict | None:
        return self.data.get("active")

    def _engine(self) -> Engine:
        if not self.active:
            raise error("no_training")
        return Engine(self.active)

    def _resolve_workout(self, plan_id: str | None, workout_id: str | None) -> tuple[str, str]:
        if plan_id is None:
            nxt = self.data.get("next")
            if not nxt:
                raise error("no_plan")
            plan_id = nxt["plan_id"]
            workout_id = workout_id or nxt["workout_id"]
        plan = self._plan(plan_id)
        workout_id = workout_id or plan["workouts"][0]["id"]
        try:
            find_workout(plan, workout_id)
        except KeyError as err:
            raise error("workout_not_found", workout=workout_id, plan=plan_id) from err
        return plan_id, workout_id

    def _resolve_satellite(self, satellite: str | None, device_id: str | None) -> str | None:
        if satellite:
            return satellite
        if device_id:
            registry = er.async_get(self.hass)
            for ent in er.async_entries_for_device(registry, device_id):
                if ent.domain == SAT_DOMAIN:
                    return ent.entity_id
        return self.default_satellite

    @property
    def default_satellite(self) -> str | None:
        """Satellit der Person, sonst der Standard aus den Optionen."""
        return self.profile.get("satellite") or self.entry.options.get(CONF_DEFAULT_SATELLITE) or None

    async def async_start(
        self,
        plan_id: str | None = None,
        workout_id: str | None = None,
        satellite: str | None = None,
        device_id: str | None = None,
        speak_intro: bool = True,
        light: str | None = None,
    ) -> dict[str, Any]:
        if self.active:
            raise error("already_running")
        plan_id, workout_id = self._resolve_workout(plan_id, workout_id)
        plan = self._plan(plan_id)
        workout = find_workout(plan, workout_id)
        steps = build_steps(plan, workout_id, lambda ex: self.last_sets(ex, plan_id, workout_id))
        self._attach_images(steps, plan_id)
        state = new_session(
            lang=self.voice_lang,
            session_id=uuid.uuid4().hex[:12],
            plan=plan,
            plan_id=plan_id,
            workout=workout,
            steps=steps,
            satellite=self._resolve_satellite(satellite, device_id),
            now=_now(),
        )
        state["light"] = self._resolve_light(light, state.get("satellite"))
        state["light_restore"] = self._light_snapshot(state["light"])
        self.data["active"] = state
        effects = Engine(state).start()
        intro = " ".join(e["text"] for e in effects if e["kind"] == "announce")
        if not speak_intro:
            effects = [e for e in effects if e["kind"] != "announce"]
        await self._run(effects)
        return {"session_id": state["id"], "announcement": intro}

    async def async_next(self, reps: int | None = None, weight_kg: float | None = None,
                         duration_s: int | None = None, effort: str | None = None) -> None:
        """Weiter. Mit Werten (Karte): aktueller Satz wird mit diesen Werten gespeichert.

        effort ("easy"/"normal"/"hard"): Anstrengung gleich mitgeben – dann ohne Rückfrage.
        """
        if not self.active:
            await self.async_start()
            return
        actual = {k: v for k, v in (("reps", reps), ("weight_kg", weight_kg), ("duration_s", duration_s))
                  if v is not None} or None
        active = self.active
        hold = active.get("hold")
        # Satz nach Zeit: im Countdown startet „Weiter“ sofort, im Seitenwechsel die zweite Seite;
        # während die Zeit läuft, endet der Satz von selbst (Knopf ohne Wirkung)
        if hold and not active.get("paused") and actual is None:
            if hold["phase"] == "ready":
                self._start_hold(dt_util.utcnow())
                self._changed()
                return
            if hold["phase"] == "switch":
                self._start_side(dt_util.utcnow())
                self._changed()
                return
            if hold["phase"] == "work":
                return
        # Pause vor einem Satz nach Zeit: „Weiter“ beendet die Pause und startet den Countdown
        if (not hold and actual is None and not active.get("paused") and active["phase"] == PHASE_ACTIVE
                and active.get("rest_until") and self._timed_step(active)
                and active.get("pending_question") is None):
            self._cancel_rest()
            active["rest_until"] = None
            self._sync_hold()
            self._changed()
            return
        if actual is None:
            # Werte aus Plus/Minus (Karte, Tasten, Drehregler) übernehmen, falls geändert
            adj = self.adjust_state()
            if adj and (adj["send"] or effort):
                actual = {"reps": adj["reps"], "duration_s": adj["duration"], "weight_kg": adj["weight"]}
                actual = {k: v for k, v in actual.items() if v is not None}
        if effort and actual is not None:
            actual["effort"] = effort if effort in ("easy", "hard") else None
        await self._run(self._engine().press_next(_now(), actual))

    # ------------------------------------------------------------------
    # Plus/Minus für den laufenden Satz (gemeinsam für Karte und Hardware)
    # ------------------------------------------------------------------

    def adjust_state(self) -> dict[str, Any] | None:
        """Aktuelle Werte für den laufenden Satz. Startwerte = Plan; neu bei jedem Satz."""
        active = self.active
        if not active or active["phase"] != "active" or active.get("paused"):
            return None
        idx = active["idx"]
        if not 0 <= idx < len(active["steps"]):
            return None
        step = active["steps"][idx]
        if step["type"] != "set":
            return None
        key = f"{active['id']}:{idx}:{step.get('target_weight')}"
        adj = active.get("adjust")
        if not adj or adj.get("key") != key:
            timed = bool(step.get("target_duration") or step.get("hold_max"))
            if timed:
                reps = None
            elif step.get("amrap"):
                reps = step.get("last_reps") or 10
            else:
                reps = step.get("target_reps")
            adj = {
                "key": key,
                "timed": timed,
                "open": bool(step.get("amrap") or step.get("hold_max")),
                "reps": reps,
                "duration": (step.get("target_duration") or step.get("last_duration") or 30) if timed else None,
                "weight": step.get("target_weight"),
                "weight_step": step.get("weight_step") or 1,
            }
            active["adjust"] = adj
        changed_count = (not adj["timed"] and adj["reps"] != step.get("target_reps")) or (
            adj["timed"] and adj["duration"] != step.get("target_duration"))
        adj["changed_reps"] = bool(changed_count) and not adj["open"]
        adj["changed_weight"] = adj["weight"] != step.get("target_weight")
        adj["changed"] = adj["changed_reps"] or adj["changed_weight"]
        adj["send"] = adj["changed"] or adj["open"]
        return adj

    def async_adjust(self, field: str, steps: int) -> None:
        """Wert in Schritten ändern. field: reps (bei Zeit-Sätzen: Sekunden) oder weight."""
        adj = self.adjust_state()
        if adj is None:
            raise error("no_active_set")
        if field == "weight":
            if adj["weight"] is None:
                raise error("no_weight")
            adj["weight"] = max(0, round(adj["weight"] + steps * adj["weight_step"], 2))
        elif adj["timed"]:
            # Dauer nur vor dem Start (im Countdown) änderbar
            if (self.active.get("hold") or {}).get("phase") in ("work", "switch"):
                return
            adj["duration"] = max(5, adj["duration"] + steps * 5)
        else:
            adj["reps"] = max(0, (adj["reps"] or 0) + steps)
        self._changed()

    def async_set_value(self, field: str, value: float) -> None:
        """Wert direkt setzen (Zahl-Entität)."""
        adj = self.adjust_state()
        if adj is None:
            raise error("no_active_set")
        if field == "weight":
            if adj["weight"] is None:
                raise error("no_weight")
            adj["weight"] = max(0, round(float(value), 2))
        elif adj["timed"]:
            adj["duration"] = max(0, int(value))
        else:
            adj["reps"] = max(0, int(value))
        self._changed()

    def exercise_points(self, exercise_ids: set[str], limit: int = CHART_POINTS, plan_id: str | None = None,
                        workout_id: str | None = None) -> dict[str, list[dict]]:
        """Bester Wert pro Training (Gewicht, Wdh., Dauer) für die genannten Übungen.

        Mit plan_id/workout_id nur Trainings dieses Workouts – außer es gibt dort noch keine.
        """
        if workout_id is not None:
            same = self._points(exercise_ids, limit, plan_id, workout_id)
            anywhere = self._points({e for e, pts in same.items() if not pts}, limit, None, None)
            return {**same, **anywhere}
        return self._points(exercise_ids, limit, None, None)

    def _points(self, exercise_ids: set[str], limit: int, plan_id: str | None,
                workout_id: str | None) -> dict[str, list[dict]]:
        out: dict[str, list[dict]] = {e: [] for e in exercise_ids}
        for sess in self.data["sessions"]:
            if workout_id is not None and (sess["plan_id"] != plan_id or sess["workout_id"] != workout_id):
                continue
            best: dict[str, dict] = {}
            for rec in sess["sets"]:
                ex = rec["exercise"]
                if ex not in out or rec["status"] == SET_SKIPPED:
                    continue
                pt = best.setdefault(ex, {"date": sess["started_at"], "weight_kg": None, "reps": None,
                                          "duration_s": None})
                for k in ("weight_kg", "reps", "duration_s"):
                    if rec.get(k) is not None and (pt[k] is None or rec[k] > pt[k]):
                        pt[k] = rec[k]
            for ex, pt in best.items():
                if any(pt[k] is not None for k in ("weight_kg", "reps", "duration_s")):
                    out[ex].append(pt)
        return {e: pts[-limit:] for e, pts in out.items()}

    async def async_undo(self) -> None:
        await self._run(self._engine().undo(_now()))

    async def async_skip(self) -> None:
        await self._run(self._engine().skip(_now()))

    async def async_pause(self) -> None:
        await self._run(self._engine().toggle_pause(_now()))

    async def async_finish(self) -> None:
        """Training regulär beenden: speichern, nächstes Workout vormerken."""
        await self._run(self._engine().finish(_now(), completed=True))

    async def async_abort(self, keep: bool = True) -> None:
        """Training abbrechen. keep=True: bisherige Sätze trotzdem speichern."""
        engine = self._engine()
        if not keep:
            self.active["sets"] = []
        await self._run(engine.finish(_now(), completed=False))

    async def async_log_set(self, *, text: str | None = None, reps: int | None = None,
                            weight_kg: float | None = None, duration_s: int | None = None,
                            effort: str | None = None) -> None:
        """Werte für den offenen bzw. letzten Satz setzen (z. B. aus eigener Automation)."""
        engine = self._engine()
        if text is not None:
            pending = self.active.get("pending_question")
            target = engine.find_set(pending) if pending is not None else (
                self.active["sets"][-1] if self.active["sets"] else None)
            parsed = parse_answer(text, timed=bool(target and (target.get("target_duration") or target.get("hold_max"))),
                                  lang=self.active.get("lang", "de"))
        else:
            values = {"reps": reps, "weight_kg": weight_kg, "duration_s": duration_s}
            parsed = {"kind": "correct" if any(v is not None for v in values.values()) else "confirm", **values}
        if effort:
            parsed["effort"] = effort if effort in ("easy", "hard") else None
        pending = self.active.get("pending_question")
        if pending is not None:
            await self._run(engine.answer(pending, parsed, _now()))
            return
        if not self.active["sets"]:
            raise error("no_sets_yet")
        last = self.active["sets"][-1]
        if last["status"] == SET_PLANNED:
            # stummer Modus: wie eine Antwort auf die Rückfrage behandeln
            await self._run(engine.answer(last["id"], parsed, _now()))
        elif parsed["kind"] in ("correct", "confirm") and (parsed["kind"] == "correct" or "effort" in parsed):
            changes = {k: parsed[k] for k in ("reps", "weight_kg", "duration_s") if parsed.get(k) is not None}
            if "effort" in parsed:
                changes["effort"] = parsed["effort"]
            self.edit_set(None, last["id"], changes)
        elif parsed["kind"] == "skip":
            self.edit_set(None, last["id"], {"skipped": True})

    # ------------------------------------------------------------------
    # Effekte ausführen
    # ------------------------------------------------------------------

    async def _run(self, effects: Effects) -> None:
        active = self.active
        for eff in effects:
            kind = eff["kind"]
            if kind == "announce":
                sat = active and active.get("satellite")
                if sat and self.entry.options.get(CONF_ANNOUNCE, True):
                    self._voice_queue.put_nowait(("announce", sat, eff["text"]))
            elif kind == "ask":
                sat = active and active.get("satellite")
                if sat and self.entry.options.get(CONF_ASK_AFTER_SET, True):
                    Engine(active).question_started(eff["set_id"])
                    rec = Engine(active).find_set(eff["set_id"])
                    self._voice_queue.put_nowait(
                        ("ask", sat, eff["text"], active["id"], eff["set_id"], bool(rec and (rec.get("target_duration") or rec.get("hold_max"))))
                    )
            elif kind == "rest":
                self._start_rest(eff["seconds"])
            elif kind == "rest_cancel":
                self._cancel_rest()
                if active:
                    active["rest_until"] = None
                    active.pop("rest_remaining", None)
            elif kind == "block_timer":
                self._start_block_timer(eff["seconds"])
            elif kind == "block_timer_cancel":
                self._cancel_block_timer()
                if active:
                    active.pop("block_until", None)
                    active.pop("block_remaining", None)
            elif kind == "interval_start":
                self._start_interval()
            elif kind == "interval_stop":
                self._stop_interval()
            elif kind == "pause":
                self._pause_timers()
            elif kind == "resume":
                self._resume_timers()
            elif kind == "event":
                if eff["type"] == "set_answered" and self._ask_cancel:
                    self._ask_cancel.set()
                self._fire({"type": eff["type"], "session_id": active["id"] if active else None, **eff["data"]})
                if eff["type"] in ("set_logged", "set_answered") and active:
                    self._check_record(eff["data"]["set_id"])
            elif kind == "finished":
                self._archive()
                active = None
        self._sync_hold()
        self._changed()

    def _archive(self) -> None:
        active = self.active
        if not active:
            return
        self._cancel_hold()
        self._cancel_rest()
        self._cancel_block_timer()
        self._stop_interval()
        active["finished_at"] = _now()
        self._end_pause(active)  # beendet während der Pause: Pausenzeit trotzdem abziehen
        record = {
            key: active[key]
            for key in ("id", "plan_id", "plan_name", "workout_id", "workout_name", "started_at", "finished_at",
                        "status", "sets")
        }
        record["paused_s"] = round(active.get("paused_s") or 0)
        # Mit „Beenden“ vor dem letzten Schritt beendet (regulär steht idx hinter dem letzten Schritt)
        if active["status"] == "finished" and active["idx"] < len(active["steps"]):
            record["ended_early"] = True
        for rec in record["sets"]:
            if rec["status"] == SET_PENDING:
                rec["status"] = SET_UNCONFIRMED
        if record["sets"]:
            self.data["sessions"].append(record)
        if active["status"] == "finished":
            self._advance_rotation(active["plan_id"], active["workout_id"])
        self.data["active"] = None
        self.data["last_session_id"] = record["id"] if record["sets"] else None
        # Sofort speichern (nicht erst nach der kurzen Verzögerung): erst danach zeigt die Karte den Abschluss
        self._saving = self.hub.save_now()

    # -- Abschluss eines Trainings -------------------------------------------

    # Vorschläge, die als Ausblick erscheinen (ohne „Planwerte“/„wie zuletzt“), und die, bei denen es mehr wird
    OUTLOOK_KEYS = {"time_add", "time_easy_add", "time_repeat", "all_reps_add_weight", "easy_add_weight",
                    "all_done_add_weight", "all_reps_add_reps", "easy_add_reps", "easy_target", "hold_weight_target",
                    "target_reps", "harder_variant", "cap_reached", "hard_hold", "repeat_target", "not_all_hold"}
    OUTLOOK_UP = {"time_add", "time_easy_add", "all_reps_add_weight", "easy_add_weight", "all_done_add_weight",
                  "all_reps_add_reps", "easy_add_reps", "easy_target", "hold_weight_target", "target_reps",
                  "harder_variant"}

    async def async_session_summary(self, session_id: str | None = None) -> dict[str, Any] | None:
        """Zusammenfassung eines gespeicherten Trainings (wie Hero Upgrade sessionSummary). Wartet aufs Speichern."""
        if self._saving and not self._saving.done():
            await self._saving
        sid = session_id or self.data.get("last_session_id")
        sessions = self.data["sessions"]
        sess = next((x for x in sessions if x["id"] == sid), None)
        if not sess:
            return None
        done = [r for r in sess["sets"] if st.counts(r)]

        def sides(rec: dict) -> int:
            # einseitige Sätze gelten für beide Seiten; Flow-Abschnitte (mit side) sind schon je Seite gespeichert
            return 2 if rec.get("per_side") and not rec.get("side") else 1

        reps = time_s = 0
        volume = 0.0
        group_count: dict[str, int] = {}
        exercises: set[str] = set()
        for rec in done:
            exercises.add(rec["exercise"])
            if isinstance(rec.get("reps"), (int, float)):
                reps += rec["reps"] * sides(rec)
            if isinstance(rec.get("duration_s"), (int, float)):
                time_s += rec["duration_s"] * sides(rec)
            if rec.get("weight_kg") and isinstance(rec.get("reps"), (int, float)):
                volume += rec["weight_kg"] * rec["reps"] * sides(rec)
            for g in self.groups_of(rec, sess):
                group_count[g] = group_count.get(g, 0) + 1
        muscles = [g for g, _ in sorted(group_count.items(), key=lambda x: -x[1])]
        records = [{"name": r["exercise_name"], **r["record"]} for r in sess["sets"] if r.get("record")]

        # Vergleich mit dem letzten Mal desselben Workouts (Verlauf ist zeitlich sortiert): bester Wert je Übung
        pos = sessions.index(sess)
        before = next((x for x in reversed(sessions[:pos]) if x["plan_id"] == sess["plan_id"]
                       and x["workout_id"] == sess["workout_id"] and any(st.counts(r) for r in x["sets"])), None)

        def best(sets: list[dict]) -> dict[str, dict]:
            out: dict[str, dict] = {}
            for rec in (r for r in sets if st.counts(r)):
                b = out.setdefault(rec["exercise"], {"name": rec["exercise_name"], "weight_kg": None, "reps": None,
                                                     "duration_s": None})
                for k in ("weight_kg", "reps", "duration_s"):
                    v = rec.get(k)
                    if isinstance(v, (int, float)) and (b[k] is None or v > b[k]):
                        b[k] = v
            return out

        improved: list[dict] = []
        comparison = None
        if before:
            now_b, then_b = best(sess["sets"]), best(before["sets"])
            for ex, b in now_b.items():
                o = then_b.get(ex)
                if not o:
                    continue
                # Gewicht zuerst; bei gleichem Gewicht zählen mehr Wiederholungen bzw. längere Zeit
                if b["weight_kg"] is not None and o["weight_kg"] is not None and b["weight_kg"] > o["weight_kg"]:
                    improved.append({"name": b["name"], "kind": "weight", "before": o["weight_kg"], "now": b["weight_kg"]})
                elif (b["reps"] is not None and o["reps"] is not None and b["reps"] > o["reps"]
                      and (b["weight_kg"] or 0) >= (o["weight_kg"] or 0)):
                    improved.append({"name": b["name"], "kind": "reps", "before": o["reps"], "now": b["reps"]})
                elif b["duration_s"] is not None and o["duration_s"] is not None and b["duration_s"] > o["duration_s"]:
                    improved.append({"name": b["name"], "kind": "duration", "before": o["duration_s"],
                                     "now": b["duration_s"]})
            prev_done = [r for r in before["sets"] if st.counts(r)]
            prev_volume = sum(r["weight_kg"] * r["reps"] * sides(r) for r in prev_done
                              if r.get("weight_kg") and isinstance(r.get("reps"), (int, float)))
            comparison = {"date": before["started_at"], "duration_s": round(st.duration_min(before) * 60),
                          "sets": len(prev_done), "volume_kg": round(prev_volume)}

        # Ausblick: Vorschläge der Progression für das nächste Mal dieses Workouts (gleiche Logik wie die Vorschau)
        outlook: list[dict] = []
        if sess["status"] == "finished" and sess["plan_id"] in self.data["plans"]:
            try:
                seen: set[str] = set()
                for step in self.preview(sess["plan_id"], sess["workout_id"]):
                    if step["type"] != "set" or step["exercise"] in seen or step["exercise"] not in exercises:
                        continue
                    seen.add(step["exercise"])
                    if step.get("suggestion_key") not in self.OUTLOOK_KEYS:
                        continue
                    outlook.append({"name": step["exercise_name"], "key": step["suggestion_key"],
                                    "params": step.get("suggestion_params") or {}, "text": step.get("suggestion"),
                                    "weight_kg": step.get("target_weight"), "reps": step.get("target_reps"),
                                    "up": step["suggestion_key"] in self.OUTLOOK_UP})
                outlook.sort(key=lambda o: not o["up"])
            except (HomeAssistantError, KeyError):
                outlook = []  # Plan/Workout nicht mehr vorhanden: kein Ausblick

        today = dt_util.now().date()
        goal = self.profile.get("weekly_goal", DEFAULT_WEEKLY_GOAL)
        per_week = st.weekly_counts(sessions, self._local_day)
        week = st.week_summary(sessions, today, self._local_day, self.groups_of, goal)
        seed = 7
        for ch in str(sess["id"]):
            seed = (seed * 31 + ord(ch)) % 4294967296
        return {
            "id": sess["id"], "status": sess["status"], "ended_early": bool(sess.get("ended_early")),
            "workout_name": sess["workout_name"], "plan_name": sess["plan_name"],
            "duration_s": round(st.duration_min(sess) * 60),
            "exercises": len(exercises), "sets": len(done), "reps": reps, "time_s": time_s,
            "volume_kg": round(volume), "muscles": muscles, "records": records, "improved": improved,
            "comparison": comparison, "outlook": outlook[:6],
            "week_done": week["done"], "week_goal": goal,
            "streak_weeks": st.streak_weeks(per_week, today, self._goal_of()),
            "total": sum(per_week.values()),
            # Wechselnde Überschrift: fest je Training, damit sie beim Neuzeichnen nicht springt
            "seed": seed,
        }

    # -- Pausentimer -----------------------------------------------------

    def _start_rest(self, seconds: float) -> None:
        self._cancel_rest()
        if not self.active or seconds <= 0:
            return
        self.active["rest_until"] = (dt_util.utcnow() + timedelta(seconds=seconds)).isoformat()
        self.active.pop("rest_remaining", None)
        self._rest_unsub = async_call_later(self.hass, seconds, self._rest_over)

    def _cancel_rest(self) -> None:
        if self._rest_unsub:
            self._rest_unsub()
            self._rest_unsub = None

    @callback
    def _rest_over(self, _now: Any) -> None:
        self._rest_unsub = None
        active = self.active
        if not active:
            return
        active["rest_until"] = None
        self._fire({"type": "rest_over", "session_id": active["id"]})
        self._sync_hold()  # Pause vor einem Satz nach Zeit vorbei: Countdown beginnt
        sat = active.get("satellite")
        if sat and self.entry.options.get(CONF_ANNOUNCE, True):
            self._voice_queue.put_nowait(("announce", sat, Speech(active.get("lang", "de")).t("rest_over")))
        self._notify(Speech(active.get("lang", "de")).t("rest_over"))
        self._changed()

    @staticmethod
    def _end_pause(active: dict) -> None:
        """Laufende Pause abschließen: Dauer zu paused_s addieren (die Trainingsuhr zählt Pausen nicht mit)."""
        started = active.pop("paused_at", None)
        if started:
            pause = (dt_util.utcnow() - dt_util.parse_datetime(started)).total_seconds()
            active["paused_s"] = (active.get("paused_s") or 0) + max(0, pause)

    def _pause_timers(self) -> None:
        active = self.active
        if active and not active.get("paused_at"):
            active["paused_at"] = _now()
        for key in ("rest", "block"):
            if active and active.get(f"{key}_until"):
                until = dt_util.parse_datetime(active[f"{key}_until"])
                active[f"{key}_remaining"] = max(0, (until - dt_util.utcnow()).total_seconds())
                active[f"{key}_until"] = None
        self._cancel_rest()
        self._cancel_block_timer()
        if self._interval_task:
            self._interval_task.cancel()
            self._interval_task = None
        hold = active and active.get("hold")
        if hold and hold.get("until"):
            hold["remaining"] = max(0, (dt_util.parse_datetime(hold["until"]) - dt_util.utcnow()).total_seconds())
            hold["until"] = None
        self._cancel_hold()

    def _resume_timers(self) -> None:
        active = self.active
        if not active:
            return
        self._end_pause(active)
        remaining = active.pop("rest_remaining", None)
        if remaining:
            self._start_rest(remaining)
        block_remaining = active.pop("block_remaining", None)
        if block_remaining:
            self._start_block_timer(block_remaining)
        if active["phase"] == PHASE_INTERVAL:
            self._start_interval()
        hold = active.get("hold")
        if hold and hold.get("remaining") is not None:
            remaining = hold.pop("remaining")
            hold["until"] = (dt_util.utcnow() + timedelta(seconds=remaining)).isoformat()
            self._schedule_hold()

    # -- Satz nach Zeit: 5 s Countdown (Dauer noch änderbar), dann läuft die Zeit und der Satz wird am Ende von
    #    selbst eingetragen. Einseitig: Seite 1 → Wechselpause (SIDE_SWITCH_S, mit Ansage) → Seite 2; die Zeit
    #    gilt pro Seite. Gleicher Ablauf wie Hero Upgrade (trainer.ts). --------------------------------------

    @staticmethod
    def _timed_step(active: dict) -> dict | None:
        idx = active["idx"]
        step = active["steps"][idx] if 0 <= idx < len(active["steps"]) else None
        if step and step["type"] == "set" and (step.get("target_duration") or step.get("hold_max")):
            return step
        return None

    def _sync_hold(self) -> None:
        """Countdown anlegen, sobald ein Satz nach Zeit dran ist und keine Pause mehr läuft; Veraltetes entfernen."""
        active = self.active
        if not active:
            self._cancel_hold()
            return
        key = f"{active['idx']}:{len(active['sets'])}"
        hold = active.get("hold")
        if hold and hold.get("key") != key:
            active["hold"] = hold = None
            self._cancel_hold()
        if (not hold and self._timed_step(active) and active["phase"] == PHASE_ACTIVE and not active.get("paused")
                and not active.get("rest_until")):
            until = dt_util.utcnow() + timedelta(seconds=HOLD_COUNTDOWN_S)
            active["hold"] = {"key": key, "phase": "ready", "until": until.isoformat()}
            self._fire({"type": "hold_ready", "session_id": active["id"]})
            self._schedule_hold()

    def _schedule_hold(self) -> None:
        self._cancel_hold()
        hold = (self.active or {}).get("hold")
        if not hold or not hold.get("until"):
            return
        seconds = max(0.0, (dt_util.parse_datetime(hold["until"]) - dt_util.utcnow()).total_seconds())
        self._hold_unsub = async_call_later(self.hass, seconds, self._hold_due)

    def _cancel_hold(self) -> None:
        if self._hold_unsub:
            self._hold_unsub()
            self._hold_unsub = None

    def _start_hold(self, at: Any) -> None:
        """Zeit beginnt (ab `at`). Einseitig: erst Seite 1."""
        active = self.active
        hold = active.get("hold") if active else None
        if not hold:
            return
        adj = self.adjust_state()
        step = self._timed_step(active)
        hold.update(phase="work", total=(adj or {}).get("duration") or 30, sides=2 if step and step.get("per_side") else 1,
                    side=1, until=(at + timedelta(seconds=(adj or {}).get("duration") or 30)).isoformat())
        self._fire({"type": "hold_go", "session_id": active["id"],
                                              "side": 1 if hold["sides"] == 2 else None})
        self._schedule_hold()

    def _start_switch(self, at: Any) -> None:
        """Seite 1 ist um: Wechselpause mit Ansage."""
        active = self.active
        hold = active["hold"]
        step = self._timed_step(active)
        hold.update(phase="switch", switch_total=(step or {}).get("side_switch_s") or SIDE_SWITCH_S)
        hold["until"] = (at + timedelta(seconds=hold["switch_total"])).isoformat()
        self._fire({"type": "hold_switch", "session_id": active["id"]})
        sat = active.get("satellite")
        if sat and self.entry.options.get(CONF_ANNOUNCE, True):
            self._voice_queue.put_nowait(("announce", sat, Speech(active.get("lang", "de")).t("side_switch")))
        self._schedule_hold()

    def _start_side(self, at: Any) -> None:
        """Seite 2 beginnt."""
        active = self.active
        hold = active["hold"]
        hold.update(phase="work", side=2, until=(at + timedelta(seconds=hold["total"])).isoformat())
        self._fire({"type": "hold_go", "session_id": active["id"], "side": 2})
        self._schedule_hold()

    @callback
    def _hold_due(self, _now: Any) -> None:
        self._hold_unsub = None
        active = self.active
        hold = active.get("hold") if active else None
        if not hold or active.get("paused") or not hold.get("until"):
            return
        at = dt_util.parse_datetime(hold["until"])
        if hold["phase"] == "ready":
            self._start_hold(at)
        elif hold["phase"] == "work" and hold.get("sides") == 2 and hold.get("side") == 1:
            self._start_switch(at)
        elif hold["phase"] == "switch":
            self._start_side(at)
        elif hold["phase"] == "work":
            # Zeit um: Satz mit der geplanten (bzw. im Countdown angepassten) Zeit eintragen, ohne Rückfrage
            adj = self.adjust_state()
            values: dict[str, Any] = {"duration_s": hold["total"]}
            if adj and adj.get("weight") is not None:
                values["weight_kg"] = adj["weight"]
            active["hold"] = None
            self._fire({"type": "hold_done", "session_id": active["id"]})
            self.hass.async_create_task(self.async_next(**values))
            return
        self._changed()

    # -- Zeitlimit eines Blocks („5 Minuten im Wechsel“) -----------------

    def _start_block_timer(self, seconds: float) -> None:
        self._cancel_block_timer()
        if not self.active:
            return
        self.active["block_until"] = (dt_util.utcnow() + timedelta(seconds=seconds)).isoformat()
        self.active["block_expired"] = False
        self._block_unsub = async_call_later(self.hass, seconds, self._block_time_over)

    def _cancel_block_timer(self) -> None:
        if self._block_unsub:
            self._block_unsub()
            self._block_unsub = None

    @callback
    def _block_time_over(self, _now: Any) -> None:
        self._block_unsub = None
        active = self.active
        if not active:
            return
        active["block_until"] = None
        active["block_expired"] = True
        self._fire({"type": "time_cap_over", "session_id": active["id"]})
        sat = active.get("satellite")
        if sat and self.entry.options.get(CONF_ANNOUNCE, True):
            self._voice_queue.put_nowait(
                ("announce", sat, Speech(active.get("lang", "de")).t("time_cap_over"))
            )
        self._changed()

    # -- HIIT ------------------------------------------------------------

    def _start_interval(self) -> None:
        self._stop_interval()
        self._interval_task = self.entry.async_create_background_task(
            self.hass, self._interval_runner(self.active["id"]), f"{DOMAIN}_interval"
        )

    def _stop_interval(self) -> None:
        if self._interval_task:
            self._interval_task.cancel()
            self._interval_task = None

    async def _interval_runner(self, session_id: str) -> None:
        """Zeitgesteuerter Block (HIIT/Flow): Abschnitte nacheinander, jeder fertige Abschnitt wird als Satz gespeichert."""
        active = self.active
        if not active or active["id"] != session_id:
            return
        step = active["steps"][active["idx"]]
        segs = step.get("segments") or [  # Sessions von vor den Abschnitten
            {"exercise": (step.get("exercises") or [None])[(r - 1) % max(1, len(step.get("exercises") or [1]))],
             "name": step["exercise_names"][(r - 1) % len(step["exercise_names"])], "side": None,
             "work_s": step["work_s"], "rest_s": step["rest_s"] if r < step["rounds"] else 0}
            for r in range(1, step["rounds"] + 1)
        ]
        sp = Speech(active.get("lang", "de"))
        flow = step.get("block_type") == "flow"
        sat = active.get("satellite") if self.entry.options.get(CONF_ANNOUNCE, True) else None
        start = (active.get("interval") or {}).get("round", 1)
        count = len(segs)
        for i in range(start, count + 1):
            seg = segs[i - 1]
            label = sp.segment_name(seg)
            nxt = sp.segment_name(segs[i]) if i < count else None
            if sat and (flow or i == 1):
                self._voice_queue.put_nowait(("announce", sat, sp.t("flow_go" if flow else "interval_go", exercise=label)))
            for phase, seconds in (("work", seg["work_s"]), ("rest", seg["rest_s"])):
                if seconds <= 0:
                    continue
                active["interval"] = {
                    "round": i,
                    "rounds": count,
                    "phase": phase,
                    "flow": flow,
                    "exercise": label if phase == "work" else nxt,
                    "image": self.image_for(seg["exercise"] if phase == "work" else (segs[i]["exercise"] if i < count else ""),
                                            active["plan_id"]) if seg.get("exercise") else None,
                    "ends_at": (dt_util.utcnow() + timedelta(seconds=seconds)).isoformat(),
                }
                self._fire({"type": f"interval_{phase}", "session_id": session_id, "round": i, "rounds": count,
                            "exercise": active["interval"]["exercise"], "seconds": seconds})
                self._changed()
                await asyncio.sleep(seconds)
                if phase == "work":
                    rec = Engine(active).log_segment({**seg, "index": i, "count": count}, _now())
                    if rec:
                        self._check_record(rec["id"])
        self._interval_task = None
        await self._run(Engine(active).interval_done())

    # -- Sprache ---------------------------------------------------------

    async def _voice_worker(self) -> None:
        while True:
            item = await self._voice_queue.get()
            try:
                if item[0] == "announce":
                    await self._announce(item[1], item[2])
                else:
                    await self._ask(*item[1:])
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 – Sprache darf das Training nie stoppen
                _LOGGER.exception("Sprachausgabe/Rückfrage fehlgeschlagen")

    async def _sat_call(self, service: str, data: dict[str, Any], *, response: bool = False) -> Any:
        if not self.hass.services.has_service(SAT_DOMAIN, service):
            _LOGGER.warning("Aktion %s.%s nicht verfügbar – ist ein Assist-Satellit eingerichtet?",
                            SAT_DOMAIN, service)
            return None
        try:
            return await self.hass.services.async_call(
                SAT_DOMAIN, service, {**data, "preannounce": False}, blocking=True, return_response=response
            )
        except vol.Invalid:
            # ältere HA-Versionen ohne "preannounce"
            return await self.hass.services.async_call(
                SAT_DOMAIN, service, data, blocking=True, return_response=response
            )

    async def _announce(self, satellite: str, text: str) -> None:
        _LOGGER.debug("Ansage an %s: %s", satellite, text)
        await self._sat_call("announce", {"entity_id": satellite, "message": text})

    async def _ask(self, satellite: str, text: str, session_id: str, set_id: int, timed: bool) -> None:
        active = self.active
        if not active or active["id"] != session_id or active.get("pending_question") != set_id:
            return  # schon per Knopf beantwortet
        _LOGGER.debug("Rückfrage an %s: %s", satellite, text)
        self._ask_cancel = cancel = asyncio.Event()
        ask_task = self.hass.async_create_task(
            self._sat_call("ask_question", {"entity_id": satellite, "question": text}, response=True)
        )
        cancel_task = self.hass.async_create_task(cancel.wait())
        timeout = self.entry.options.get(CONF_QUESTION_TIMEOUT, DEFAULT_QUESTION_TIMEOUT)
        done, _ = await asyncio.wait({ask_task, cancel_task}, timeout=timeout,
                                     return_when=asyncio.FIRST_COMPLETED)
        for task in (ask_task, cancel_task):
            if not task.done():
                task.cancel()
        self._ask_cancel = None
        if cancel_task in done:
            return  # Knopf/Karte war schneller
        sentence = None
        if ask_task in done and not ask_task.cancelled() and ask_task.exception() is None:
            resp = ask_task.result()
            if isinstance(resp, dict) and satellite in resp and isinstance(resp[satellite], dict):
                resp = resp[satellite]
            if isinstance(resp, dict):
                sentence = resp.get("sentence")
        elif ask_task in done and not ask_task.cancelled():
            _LOGGER.warning("Rückfrage fehlgeschlagen: %s", ask_task.exception())
        parsed = parse_answer(sentence, timed=timed, lang=active.get("lang", "de") if active else "de")
        _LOGGER.debug("Antwort %r → %s", sentence, parsed)
        active = self.active
        if not active or active["id"] != session_id:
            return
        await self._run(Engine(active).answer(set_id, parsed, _now()))

    # ------------------------------------------------------------------
    # Profile (mehrere Personen)
    # ------------------------------------------------------------------

    @property
    def profile(self) -> dict[str, Any]:
        return self.data["profiles"][self.pid]

    def set_weekly_goal(self, goal: int) -> None:
        """Wochenziel ändern. Gilt ab dieser Woche; frühere Wochen behalten ihr damaliges Ziel (für die Serie)."""
        prof = self.profile
        new = max(1, min(14, int(goal)))
        history = prof.setdefault("goal_history", {})
        if not history:
            history["1970-01-05"] = prof.get("weekly_goal", DEFAULT_WEEKLY_GOAL)  # alles davor: bisheriges Ziel
        history[st.week_start(dt_util.now().date()).isoformat()] = new
        prof["weekly_goal"] = new
        self._changed()

    def _goal_of(self) -> Any:
        prof = self.profile
        current = prof.get("weekly_goal", DEFAULT_WEEKLY_GOAL)
        history = prof.get("goal_history", {})
        return lambda week: st.goal_for_week(history, week, current)

    # ------------------------------------------------------------------
    # Auswertungen: Woche, Serie, Muskelgruppen, Erholung, Rekorde
    # ------------------------------------------------------------------

    def _muscle_info(self, exercise_id: str, plan_id: str | None) -> tuple[list[str], list[str], bool]:
        """(Hauptgruppen, Nebengruppen, im Plan festgelegt?). `muscles` im Plan hat Vorrang vor dem Katalogbild.

        Nebengruppen (Katalog: secondaryMuscles) zählen nur für die Erholung, nicht für das Wochenvolumen.
        """
        key = (plan_id, exercise_id)
        if key not in self._groups_cache:
            plans = [self.data["plans"][plan_id]] if plan_id in self.data["plans"] else []
            plans += [p for p in self.data["plans"].values() if p["id"] != plan_id]
            for stored in plans:
                ex = stored["data"]["exercises"].get(exercise_id)
                if ex is not None and "muscles" in ex:
                    self._groups_cache[key] = ([g for g in ex["muscles"] if g in st.GROUP_ORDER], [], True)
                    break
            else:
                cid = self.catalog_id_for(exercise_id, plan_id)
                entry = self._catalog.by_id.get(cid, {}) if self._catalog and cid else {}
                primary = st.groups_for(entry.get("muscles", []))
                secondary = [g for g in st.groups_for(entry.get("secondary", [])) if g not in primary]
                self._groups_cache[key] = (primary, secondary, False)
        return self._groups_cache[key]

    def groups_of(self, rec: dict, sess: dict | None = None) -> list[str]:
        """Muskelgruppen einer Übung (aus dem Plan, sonst über den Übungskatalog, siehe images.py)."""
        return self._muscle_info(rec["exercise"], (sess or {}).get("plan_id"))[0]

    def secondary_groups_of(self, rec: dict, sess: dict | None = None) -> list[str]:
        """Nebengruppen (zählen für die Erholung mit Vorsprung, siehe stats.SECONDARY_HEAD_START_H)."""
        return self._muscle_info(rec["exercise"], (sess or {}).get("plan_id"))[1]

    def _unassigned(self, today) -> dict[str, Any]:
        """Sätze dieser Woche ohne Muskelgruppe (weder Katalogbild noch `muscles` im Plan)."""
        start = st.week_start(today)
        sets, names = 0, set()
        for sess in self.data["sessions"]:
            if st.week_start(self._local_day(sess["started_at"])) != start:
                continue
            for rec in sess["sets"]:
                if not st.counts(rec):
                    continue
                groups, _, explicit = self._muscle_info(rec["exercise"], sess.get("plan_id"))
                if not groups and not explicit:
                    sets += 1
                    names.add(rec["exercise_name"])
        return {"sets": sets, "names": sorted(names)}

    @staticmethod
    def _local_day(iso: str):
        return dt_util.as_local(dt_util.parse_datetime(iso)).date()

    def _program_groups(self) -> set[str]:
        plan_id = self.data.get("program")
        stored = self.data["plans"].get(plan_id)
        if not stored:
            return set()
        return {g for ex in stored["data"]["exercises"]
                for g in self.groups_of({"exercise": ex}, {"plan_id": plan_id})}

    def stats(self) -> dict[str, Any]:
        sessions = self.data["sessions"]
        today = dt_util.now().date()
        goal = self.profile.get("weekly_goal", DEFAULT_WEEKLY_GOAL)
        per_week = st.weekly_counts(sessions, self._local_day)
        records = []
        for sess in reversed(sessions):
            for rec in sess["sets"]:
                if rec.get("record"):
                    records.append({"date": sess["started_at"], "exercise": rec["exercise"],
                                    "name": rec["exercise_name"], **rec["record"]})
            if len(records) >= 8:
                break
        return {
            "week": st.week_summary(sessions, today, self._local_day, self.groups_of, goal),
            "streak_weeks": st.streak_weeks(per_week, today, self._goal_of()),
            "total": sum(per_week.values()),
            "first": next((x["started_at"] for x in sessions if any(st.counts(r) for r in x["sets"])), None),
            "time": st.time_stats(sessions, today, self._local_day),
            "volume": st.muscle_volume(sessions, today, self._local_day, self.groups_of),
            "unassigned": self._unassigned(today),
            "recovery": st.recovery(sessions, dt_util.utcnow(), self.groups_of, self._program_groups(), self.secondary_groups_of),
            "recovery_tier_hours": list(st.RECOVERY_TIER_HOURS),
            "records": records[:8],
        }

    def _last_same_duration(self) -> int | None:
        """Dauer (s) des letzten abgeschlossenen Trainings mit demselben Workout – Vergleich zur laufenden Zeit."""
        active = self.active
        if not active:
            return None
        for sess in reversed(self.data["sessions"]):
            if (sess["plan_id"] == active["plan_id"] and sess["workout_id"] == active["workout_id"]
                    and sess.get("status") == "finished" and sess.get("finished_at")):
                minutes = st.duration_min(sess)
                if minutes > 0:
                    return round(minutes * 60)
        return None

    def week_info(self) -> dict[str, Any]:
        """Leichtgewichtig für Sensoren: Trainings diese Woche, Ziel, Serie in Wochen."""
        today = dt_util.now().date()
        goal = self.profile.get("weekly_goal", DEFAULT_WEEKLY_GOAL)
        per_week = st.weekly_counts(self.data["sessions"], self._local_day)
        return {"done": per_week.get(st.week_start(today), 0), "goal": goal,
                "streak_weeks": st.streak_weeks(per_week, today, self._goal_of()), "total": sum(per_week.values())}

    def _check_record(self, set_id: int) -> None:
        """Nach einem erfassten Satz: neuer Bestwert? Dann Ansage, Event und Handy-Hinweis."""
        active = self.active
        rec = Engine(active).find_set(set_id) if active else None
        if not rec or rec.get("record_checked") or rec["status"] not in RECORD_STATUSES:
            return
        rec["record_checked"] = True
        previous = [x for sess in self.data["sessions"] for x in sess["sets"] if x["exercise"] == rec["exercise"]]
        previous += [x for x in active["sets"] if x["exercise"] == rec["exercise"] and x["id"] != rec["id"]]
        found = st.new_record(rec, previous)
        if not found:
            return
        rec["record"] = found
        sp = Speech(active.get("lang", "de"))
        text = sp.record(rec["exercise_name"], found)
        sat = active.get("satellite")
        if sat and self.entry.options.get(CONF_ANNOUNCE, True):
            self._voice_queue.put_nowait(("announce", sat, text))
        self._notify(text)
        self._flash_light("record")
        self._fire({"type": "record", "session_id": active["id"],
                                              "exercise": rec["exercise_name"], **found})

    # -- Lichtsignal (glow.py) -------------------------------------------

    def _resolve_light(self, light: str | None, satellite: str | None) -> str | None:
        """Lampe: beim Start angegeben → Standard aus den Optionen → Licht am Gerät des Satelliten (falls erlaubt)."""
        if light:
            return light
        if self.profile.get("light"):
            return self.profile["light"]
        if self.entry.options.get(CONF_DEFAULT_LIGHT):
            return self.entry.options[CONF_DEFAULT_LIGHT]
        if satellite and self.entry.options.get(CONF_SATELLITE_LIGHT, True):
            registry = er.async_get(self.hass)
            sat = registry.async_get(satellite)
            if sat and sat.device_id:
                lights = [e for e in er.async_entries_for_device(registry, sat.device_id)
                          if e.domain == "light" and not e.disabled_by]
                if lights:
                    return lights[0].entity_id
        return None

    def _light_snapshot(self, entity_id: str | None) -> dict[str, Any] | None:
        """Zustand der Lampe vor dem Training (zum Wiederherstellen)."""
        st_ = self.hass.states.get(entity_id) if entity_id else None
        if st_ is None:
            return None
        if st_.state != "on":
            return {"on": False}
        attrs = st_.attributes
        out: dict[str, Any] = {"on": True}
        if attrs.get("brightness") is not None:
            out["brightness"] = attrs["brightness"]
        mode = attrs.get("color_mode")
        if mode == "color_temp" and attrs.get("color_temp_kelvin"):
            out["color_temp_kelvin"] = attrs["color_temp_kelvin"]
        elif mode in ("hs", "rgb", "rgbw", "rgbww", "xy") and attrs.get("hs_color"):
            out["hs_color"] = list(attrs["hs_color"])
        return out

    def _cancel_light_timers(self) -> None:
        for name in ("_light_unsub", "_light_flash_unsub"):
            unsub = getattr(self, name)
            if unsub:
                unsub()
                setattr(self, name, None)

    @callback
    def _sync_light(self, *_: Any) -> None:
        """Lampe an den Trainingszustand anpassen (nach jeder Änderung und zum Countdown-Zeitpunkt)."""
        active = self.active
        if active and active.get("light"):
            self._light = {"entity": active["light"], "restore": active.get("light_restore")}
        if not self._light:
            return
        if self._light_unsub:
            self._light_unsub()
            self._light_unsub = None
        now = dt_util.utcnow()
        state = glow.glow_state(active, now) if active else "off"
        wait = glow.seconds_to_count(active, now)
        if wait is not None:
            self._light_unsub = async_call_later(self.hass, wait + 0.05, self._sync_light)
        if state == self._light_state:
            if not active:
                self._light = None  # Training vorbei, Lampe ist wiederhergestellt
            return
        burst = state == "work" and self._light_state in ("rest", "count", "wait")
        self._light_state = state
        light = self._light
        if active and time.monotonic() < self._light_hold_until:
            return  # Rekord leuchtet noch golden – _light_settle zeigt danach den aktuellen Zustand
        if not active:
            self._cancel_light_timers()
            self._light = None
            self._light_state = None
        self.hass.async_create_task(self._apply_light(light, state, burst))

    async def _apply_light(self, light: dict[str, Any], state: str, burst: bool = False) -> None:
        """Farbe setzen bzw. (off) den Zustand von vor dem Training wiederherstellen. Fehler stoppen nie das Training."""
        entity = light["entity"]
        try:
            if state == "off":
                restore = light.get("restore") or {"on": False}
                if not restore.get("on"):
                    await self.hass.services.async_call("light", "turn_off", {"entity_id": entity}, blocking=True)
                else:
                    data = {k: v for k, v in restore.items() if k != "on"}
                    await self.hass.services.async_call("light", "turn_on", {"entity_id": entity, **data}, blocking=True)
                return
            full = burst or state in ("count", "record")
            await self.hass.services.async_call("light", "turn_on", {
                "entity_id": entity, "rgb_color": list(glow.COLORS[state]),
                "brightness": glow.BRIGHT_FULL if full else glow.BRIGHT_SOFT}, blocking=True)
            if burst or state == "record":
                if self._light_flash_unsub:
                    self._light_flash_unsub()
                self._light_flash_unsub = async_call_later(
                    self.hass, glow.RECORD_S if state == "record" else glow.BURST_S, self._light_settle)
        except Exception:  # noqa: BLE001 – Licht darf das Training nie stoppen
            _LOGGER.warning("Lichtsignal für %s fehlgeschlagen", entity, exc_info=True)

    @callback
    def _light_settle(self, *_: Any) -> None:
        """Nach dem Aufleuchten (Wechsel in die Arbeit, Rekord) zurück zum gedämpften Zustand."""
        self._light_flash_unsub = None
        self._light_hold_until = 0.0
        if self._light and self._light_state and self.active:
            self.hass.async_create_task(self._apply_light(self._light, self._light_state))

    def _flash_light(self, kind: str) -> None:
        """Kurz aufleuchten (record = golden, bleibt glow.RECORD_S stehen)."""
        if self._light and self.active:
            self._light_hold_until = time.monotonic() + glow.RECORD_S
            self.hass.async_create_task(self._apply_light(self._light, kind))

    def _fire(self, data: dict[str, Any]) -> None:
        """Event für Automationen (Töne, Licht …) – mit der Person, damit man danach filtern kann."""
        self.hass.bus.async_fire(EVENT_NAME, {**data, "profile": self.pid, "person": self.profile["name"]})

    def _notify(self, message: str) -> None:
        """Handy-Hinweis über den notify-Dienst der Person bzw. aus den Optionen (optional)."""
        service = (self.profile.get("notify") or self.entry.options.get(CONF_NOTIFY) or "").removeprefix("notify.")
        if service and self.hass.services.has_service("notify", service):
            self.hass.async_create_task(self.hass.services.async_call(
                "notify", service, {"title": "TrainingAssistant", "message": message}))

    def async_rest_adjust(self, seconds: int) -> None:
        """Pausentimer verlängern oder verkürzen (±15 s an Karte und Tasten)."""
        active = self.active
        if not active:
            raise error("no_training")
        if active.get("paused") and active.get("rest_remaining") is not None:
            active["rest_remaining"] = max(0, active["rest_remaining"] + seconds)
        elif active.get("rest_until"):
            left = (dt_util.parse_datetime(active["rest_until"]) - dt_util.utcnow()).total_seconds() + seconds
            if left <= 1:
                self._cancel_rest()
                self._rest_over(None)
                return
            self._start_rest(left)
        elif seconds > 0:
            self._start_rest(seconds)
        self._changed()

    # ------------------------------------------------------------------
    # Zustand für Entitäten und Karte
    # ------------------------------------------------------------------

    def public_state(self) -> dict[str, Any]:
        self.adjust_state()  # Plus/Minus-Werte für den laufenden Satz aktuell halten
        active = self.active
        history: dict[str, list[dict]] = {}
        if active:
            history = self.exercise_points({s["exercise"] for s in active["steps"] if s.get("exercise")},
                                           plan_id=active["plan_id"], workout_id=active["workout_id"])
        return {
            "active": active,
            "exercise_history": history,
            "plans": [
                {
                    "id": p["id"],
                    "name": p["name"],
                    "description": p["data"].get("description"),
                    "imported_at": p["imported_at"],
                    "template": bool(p.get("template")),
                    "category": self._category_of(p),
                    "workouts": [{"id": w["id"], "name": w["name"]} for w in p["data"]["workouts"]],
                    "images_missing": [p["data"]["exercises"][k]["name"]
                                       for k, v in p.get("pictos", {}).items() if not v],
                }
                for p in self.data["plans"].values()
            ],
            "next": self.data.get("next"),
            "program": self.data.get("program"),
            "program_workouts": self.program_workouts(),
            "last_session_id": self.data.get("last_session_id"),
            "default_satellite": self.default_satellite,
            "last_same_duration_s": self._last_same_duration(),
            "side_switch_s": SIDE_SWITCH_S,
            # Alle Personen mit ihren Geräten und ob sie gerade trainieren (Karte: zuschauen/umschalten)
            "profiles": [{"id": p["id"], "name": p["name"], "user_id": p.get("user_id"),
                          "figure": p.get("figure", DEFAULT_FIGURE), "satellite": p.get("satellite"),
                          "light": p.get("light"), "notify": p.get("notify"),
                          "training": bool((self.hub.root["persons"].get(p["id"]) or {}).get("active"))}
                         for p in self.data["profiles"].values()],
            "profile": self.pid,
            "multi": True,  # mehrere Personen können gleichzeitig trainieren (Hero Upgrade: nein)
            # Übungsbilder: Figur der aktiven Person, Bilder ohne Endbild
            "figure": self.profile.get("figure", DEFAULT_FIGURE),
            "single_images": self._pictos.single() if self._pictos else [],
            "weekly_goal": self.profile.get("weekly_goal", DEFAULT_WEEKLY_GOAL),
        }

    # ------------------------------------------------------------------
    # Übungsbilder
    # ------------------------------------------------------------------

    def _lookup(self, key: str, exercise_id: str, plan_id: str | None) -> str | None:
        plans = [self.data["plans"][plan_id]] if plan_id in self.data["plans"] else []
        plans += list(self.data["plans"].values())
        for p in plans:
            value = p.get(key, {}).get(exercise_id)
            if value:
                return value
        return None

    def image_for(self, exercise_id: str, plan_id: str | None = None) -> str | None:
        """Bildname einer Übung (aus dem Plan, sonst aus irgendeinem Plan), siehe images.Pictos."""
        return self._lookup("pictos", exercise_id, plan_id)

    def catalog_id_for(self, exercise_id: str, plan_id: str | None = None) -> str | None:
        """Katalog-ID einer Übung (für die Muskelgruppen)."""
        return self._lookup("images", exercise_id, plan_id)

    def _attach_images(self, steps: list[dict], plan_id: str) -> None:
        for step in steps:
            if step.get("exercise"):
                step["image"] = self.image_for(step["exercise"], plan_id)
                primary, secondary, _ = self._muscle_info(step["exercise"], plan_id)
                step["muscles"], step["muscles_secondary"] = primary, secondary
            elif step.get("type") == "interval":
                step["images"] = [self.image_for(e, plan_id) for e in step.get("exercises", [])]

    # -- Plan-Editor (gemeinsame Oberfläche mit Hero Upgrade) ------------

    @property
    def plan_groups(self) -> list[str]:
        """Kategorien für eigene Pläne: Gruppen der Vorlagen + „other“."""
        return [*self.TEMPLATE_GROUPS, "other"]

    def _category_of(self, p: dict[str, Any]) -> str:
        """Kategorie eines Plans: eigene Wahl, sonst Gruppe der Vorlage, sonst „other“."""
        if p.get("category"):
            return p["category"]
        group = (p.get("template") or "").split("-", 1)[0]
        return group if group in self.TEMPLATE_GROUPS else "other"

    def plan_source(self, plan_id: str) -> dict[str, Any]:
        """Plan zum Bearbeiten: Daten (Editor) und Text (Import-Feld). Vorlagen-Pläne bearbeitet man als Kopie."""
        p = self.data["plans"].get(plan_id)
        if p is None:
            raise error("plan_not_found", plan=plan_id)
        return {"plan_id": plan_id, "template": bool(p.get("template")), "category": self._category_of(p),
                "plan": copy.deepcopy(p["data"]), "text": p["source"]}

    async def async_exercise_library(self) -> dict[str, Any]:
        """Alle bekannten Übungen (eigene Pläne + Vorlagen) für die Übungsauswahl im Editor."""
        templates = await self.hass.async_add_executor_job(self._read_templates)
        out: dict[str, dict[str, Any]] = {}
        names: set[str] = set()

        def add(ex_id: str, ex: dict[str, Any], cid: str | None) -> None:
            # gleiche Übung unter zwei IDs (z. B. squat/bodyweight_squat) nur einmal anbieten
            key = f"{ex['name']}|{ex.get('equipment') or ''}".lower()
            if ex_id in out or key in names:
                return
            names.add(key)
            entry = (self._catalog.by_id.get(cid) if self._catalog and cid else None) or {}
            out[ex_id] = {
                "id": ex_id, "name": ex["name"], "aliases": ex.get("aliases", []), "equipment": ex.get("equipment"),
                "image": self._pictos.match(ex_id, ex, cid) if self._pictos else None, "catalog": cid,
                "muscles": ex["muscles"] if "muscles" in ex else st.groups_for(entry.get("muscles", [])),
                "note": ex.get("note"), "unilateral": bool(ex.get("unilateral")), "explicit_muscles": "muscles" in ex,
            }

        for p in self.data["plans"].values():
            if not p.get("template"):
                for ex_id, ex in p["data"]["exercises"].items():
                    add(ex_id, ex, (p.get("images") or {}).get(ex_id))
        for t in templates:
            plan = parse_plan_text(t["text"])
            images = map_plan(plan, self._catalog) if self._catalog else {}
            for ex_id, ex in plan["exercises"].items():
                add(ex_id, ex, images.get(ex_id))
        return {"exercises": sorted(out.values(), key=lambda e: e["name"].lower()), "groups": self.plan_groups}

    def save_plan(self, plan: dict[str, Any], plan_id: str | None = None, category: str | None = None,
                  lang: str | None = None) -> dict[str, Any]:
        """Plan aus dem Editor speichern (neu oder geändert). Prüft wie beim Import; Vorlagen bleiben unverändert."""
        if not category or category not in self.plan_groups:
            raise error("category_missing")
        old = self.data["plans"].get(plan_id) if plan_id else None
        if plan_id and old is None:
            raise error("plan_not_found", plan=plan_id)
        if old and old.get("template"):
            raise error("plan_readonly")
        active = self.active
        if plan_id and active and active.get("plan_id") == plan_id:
            raise error("plan_in_use")
        data = {**plan, "schema_version": PLAN_SCHEMA_VERSION}
        text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)
        if not plan_id:
            # neue ID aus dem Namen, ohne vorhandene Pläne oder Vorlagen zu überschreiben
            base = slugify(str(data.get("name") or "plan"))
            taken = set(self.data["plans"]) | {slugify(p["name"]) for p in self.data["plans"].values()}
            plan_id, n = base, 2
            while plan_id in taken:
                plan_id, n = f"{base}_{n}", n + 1
        result = self.import_plan(text, lang, category=category, plan_id=plan_id)
        return {"plan_id": result["plan_id"], "name": result["name"]}


__all__ = ["PlanError", "TrainingManager"]
