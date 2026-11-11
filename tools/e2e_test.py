"""End-to-End-Test gegen die LOKALE Testinstanz (http://localhost:8123).

Voraussetzungen: scripts/develop läuft, TrainingAssistant ist eingerichtet, der
Test-Satellit „fake_voice“ ist geladen, Login steht in config/dev-login.txt.

Aufruf:  .venv/bin/python tools/e2e_test.py [--force]

Läuft in der Testinstanz ein Training, bricht der Test ab, statt es zu verwerfen
(mit --force wird es ohne Speichern abgebrochen).

Nicht gegen das echte Home Assistant ausführen: Der Test importiert Pläne,
startet Trainings und schreibt Verlauf.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sys

import aiohttp

BASE = "http://localhost:8123"
ROOT = Path(__file__).resolve().parent.parent
SAT = "assist_satellite.fake"

TEST_PLAN = """
schema_version: 1
name: E2E Test
exercises:
  a: {name: Übung A}
  b: {name: Übung B}
  p: {name: Pull-Ups}
  h: {name: Hampelmann}
defaults: {progression: {type: double, increment_kg: 2}}
workouts:
  - id: t
    name: Test
    blocks:
      - {type: circuit, name: Kurz, time_cap_s: 3, exercises: [{exercise: a, reps: 5, progression: {type: none}},
                                                       {exercise: b, reps: 5, progression: {type: none}}]}
      - {type: sets, exercise: p, total_reps: 10, reps: max, rest_s: 1}
      - {type: interval, rounds: 2, work_s: 1, rest_s: 1, exercises: [h]}
      - {type: cooldown}
"""

FAILED: list[str] = []


def check(cond: bool, what: str) -> None:
    print(("  ✓ " if cond else "  ✗ ") + what)
    if not cond:
        FAILED.append(what)



# Testantworten des Satelliten und erwartete Ansagen je Sprache
VOICE = {
    "de": {"answers": ["ja", "acht mal sechzehn", "", "nur sechs"], "warmup": "Aufwärmen", "effort": "acht, war schwer",
           "planned": "wie geplant", "finished": "Training beendet"},
    "en": {"answers": ["yes", "eight times sixteen", "", "only six"], "warmup": "warm-up", "effort": "eight, that was hard",
           "planned": "as planned", "finished": "Workout complete"},
}

async def login(session: aiohttp.ClientSession) -> str:
    lines = (ROOT / "config" / "dev-login.txt").read_text().splitlines()
    user = lines[1].split(": ", 1)[1]
    password = lines[2].split(": ", 1)[1]
    cid = BASE + "/"
    async with session.post(f"{BASE}/auth/login_flow", json={
        "client_id": cid, "handler": ["homeassistant", None], "redirect_uri": cid}) as r:
        flow = await r.json()
    async with session.post(f"{BASE}/auth/login_flow/{flow['flow_id']}", json={
        "username": user, "password": password, "client_id": cid}) as r:
        code = (await r.json())["result"]
    async with session.post(f"{BASE}/auth/token", data={
        "grant_type": "authorization_code", "code": code, "client_id": cid}) as r:
        return (await r.json())["access_token"]


class WS:
    def __init__(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        self.ws = ws
        self.id = 0
        self.state: dict | None = None
        self.pending: dict[int, asyncio.Future] = {}
        self.sub_id: int | None = None

    async def reader(self) -> None:
        async for msg in self.ws:
            data = json.loads(msg.data)
            if data.get("type") == "event" and data["id"] == self.sub_id:
                self.state = data["event"]
            elif data.get("type") == "result" and data["id"] in self.pending:
                self.pending.pop(data["id"]).set_result(data)

    async def call(self, **msg) -> dict:
        self.id += 1
        fut = asyncio.get_running_loop().create_future()
        self.pending[self.id] = fut
        await self.ws.send_json({"id": self.id, **msg})
        res = await asyncio.wait_for(fut, 10)
        return res

    async def service(self, domain: str, service: str, data: dict | None = None, response: bool = False) -> dict:
        return await self.call(type="call_service", domain=domain, service=service, service_data=data or {},
                               return_response=response)


async def wait_for(pred, timeout: float = 10.0) -> bool:
    end = asyncio.get_running_loop().time() + timeout
    while asyncio.get_running_loop().time() < end:
        if pred():
            return True
        await asyncio.sleep(0.1)
    return False


async def main() -> int:
    async with aiohttp.ClientSession() as session:
        token = await login(session)
        async with session.ws_connect(f"{BASE}/api/websocket") as raw:
            await raw.receive_json()
            await raw.send_json({"type": "auth", "access_token": token})
            assert (await raw.receive_json())["type"] == "auth_ok"
            ws = WS(raw)
            reader = asyncio.create_task(ws.reader())
            ws.sub_id = ws.id + 1
            await ws.call(type="training_assistant/subscribe")
            await wait_for(lambda: ws.state is not None)
            S = lambda: ws.state  # noqa: E731

            if S()["active"]:
                if "--force" not in sys.argv:
                    print("Abbruch: In der Testinstanz läuft gerade ein Training "
                          f"({S()['active']['workout_name']}). Der Test würde es verwerfen.\n"
                          "Erst beenden – oder bewusst mit --force starten.")
                    reader.cancel()
                    return 2
                await ws.service("training_assistant", "abort", {"keep": False})
            await ws.service("fake_voice", "clear")
            previous_next = S()["next"]  # am Ende wiederherstellen

            print("Import")
            for path in (ROOT / "examples" / "ganzkoerper.yaml", ROOT / "tests" / "fixtures" / "feature-testplan.yaml"):
                res = await ws.call(type="training_assistant/import_plan", text=path.read_text())
                check(res["success"], f"{path.name} importiert")
            bad = await ws.call(type="training_assistant/import_plan", text="schema_version: 1\nname: X", lang="de")
            check(not bad["success"] and "Pflichtfeld" in bad["error"]["message"], "fehlerhafter Plan abgelehnt (de)")
            bad = await ws.call(type="training_assistant/import_plan", text="schema_version: 1\nname: X", lang="en")
            check(not bad["success"] and "required field" in bad["error"]["message"], "fehlerhafter Plan abgelehnt (en)")
            res = await ws.call(type="training_assistant/import_plan", text=TEST_PLAN)
            check(res["success"], "Testplan importiert")

            res = await ws.call(type="training_assistant/templates")
            tpls = res["result"]["templates"] if res["success"] else []
            check(len(tpls) >= 33 and len({t["group_key"] for t in tpls}) == 7, f"{len(tpls)} Vorlagen in {len({t['group_key'] for t in tpls})} Gruppen")
            plans_before = len(S()["plans"])
            ok_pv = True
            for tp in tpls:
                pv = await ws.call(type="training_assistant/template_preview", template_id=tp["id"])
                wos = pv["result"]["workouts"] if pv["success"] else []
                ok_pv = ok_pv and [w["name"] for w in wos] == tp["workouts"] and all(w["steps"] for w in wos)
            check(ok_pv and len(S()["plans"]) == plans_before, "Vorschau aller Vorlagen, ohne sie zu übernehmen")
            pv = await ws.call(type="training_assistant/template_preview", template_id="gibt-es-nicht")
            check(not pv["success"], "Vorschau einer unbekannten Vorlage abgelehnt")

            # Sprache der Ansagen = Sprache der Testinstanz (Option voice_language steht dort auf „auto“)
            cfg = await ws.call(type="get_config")
            lang = "de" if str(cfg["result"].get("language", "en")).lower().startswith("de") else "en"
            V = VOICE[lang]
            print(f"Ganzkörper A mit Test-Satellit (Sprache: {lang})")
            await ws.call(type="training_assistant/set_next", plan_id="ganzkoerper_hypertrophie", workout_id="a")
            check(S()["program"] == "ganzkoerper_hypertrophie", "Ganzkörper ist aktives Programm")
            await ws.service("fake_voice", "set_answers", {"answers": V["answers"]})
            res = await ws.service("training_assistant", "start",
                                   {"plan_id": "ganzkoerper_hypertrophie", "workout_id": "a", "satellite": SAT},
                                   response=True)
            check(res["success"] and V["warmup"] in res["result"]["response"]["announcement"], "Start + Begrüßung")
            await wait_for(lambda: S()["active"] is not None)
            await ws.service("training_assistant", "next")  # Aufwärmen fertig
            await wait_for(lambda: S()["active"]["phase"] == "ready")
            check(S()["active"]["phase"] == "ready", "Zirkel wartet auf Knopf")
            await ws.service("training_assistant", "next")  # bereit
            for _ in range(4):  # 4 Sätze, Rückfragen per fake_voice
                before = len(S()["active"]["sets"])
                await ws.service("training_assistant", "next")
                await wait_for(lambda: len(S()["active"]["sets"]) > before and S()["active"]["pending_question"] is None)
            sets = S()["active"]["sets"]
            check([x["status"] for x in sets] == ["confirmed", "corrected", "unconfirmed", "corrected"],
                  f"Status der Sätze: {[x['status'] for x in sets]}")
            check(sets[1]["reps"] == 8 and sets[1]["weight_kg"] == 16, f"„{V['answers'][1]}“ übernommen")
            check(sets[3]["reps"] == 6, f"„{V['answers'][3]}“ übernommen")
            check(S()["active"]["rest_until"] is not None, "Pausentimer läuft")

            # Knopf während Rückfrage = bestätigt
            await ws.service("fake_voice", "set_answers", {"answers": []})
            await ws.service("training_assistant", "next")
            await ws.service("training_assistant", "next")  # sofort: „wie geplant“
            await wait_for(lambda: S()["active"]["pending_question"] is None)
            check(S()["active"]["sets"][-1]["status"] == "confirmed", "Knopf während Rückfrage = bestätigt")

            # Plus/Minus an der Karte: Satz mit echten Werten, ohne Rückfrage
            n = len(S()["active"]["sets"])
            log_before = len((await ws.service("fake_voice", "get_log", response=True))["result"]["response"]["log"])
            await ws.service("training_assistant", "next", {"reps": 3, "weight_kg": 14})
            await wait_for(lambda: len(S()["active"]["sets"]) > n)
            rec = S()["active"]["sets"][-1]
            check(rec["status"] == "corrected" and rec["reps"] == 3 and rec["weight_kg"] == 14,
                  f"Satz mit Kartenwerten: {rec['reps']} × {rec['weight_kg']} ({rec['status']})")
            await asyncio.sleep(0.5)
            log = (await ws.service("fake_voice", "get_log", response=True))["result"]["response"]["log"]
            check(not any(x[0] == "ask" for x in log[log_before:]), "keine Rückfrage bei Kartenwerten")

            # Korrektur an der Karte
            sid = S()["active"]["sets"][0]["id"]
            res = await ws.call(type="training_assistant/edit_set", set_id=sid, reps=15)
            check(res["success"] and res["result"]["status"] == "edited", "Satz an der Karte geändert")

            # Rückgängig
            n = len(S()["active"]["sets"])
            await ws.service("training_assistant", "undo")
            await wait_for(lambda: len(S()["active"]["sets"]) == n - 1)
            check(len(S()["active"]["sets"]) == n - 1, "Rückgängig verwirft letzten Satz")

            # Plus/Minus über die Integration (Drehregler, Tasten, Zahl-Entitäten)
            await wait_for(lambda: S()["active"].get("adjust") is not None)
            adj0 = dict(S()["active"]["adjust"])
            step = S()["active"]["steps"][S()["active"]["idx"]]
            await ws.service("training_assistant", "adjust", {"field": "reps", "steps": -2})
            if adj0["weight"] is not None:
                await ws.call(type="call_service", domain="button", service="press",
                              target={"entity_id": "button.trainingassistant_weight_up"})
            await wait_for(lambda: S()["active"]["adjust"]["changed"])
            adj = S()["active"]["adjust"]
            check(adj["reps"] == adj0["reps"] - 2, f"Wdh. per Aktion: {adj0['reps']} → {adj['reps']}")
            if adj0["weight"] is not None:
                check(adj["weight"] == adj0["weight"] + adj0["weight_step"],
                      f"Gewicht per Taste: {adj0['weight']} → {adj['weight']}")
            states = {x["entity_id"]: x for x in (await ws.call(type="get_states"))["result"]}
            num = states.get("number.trainingassistant_reps_current_set")
            check(num is not None and float(num["state"]) == adj["reps"], f"Zahl-Entität zeigt {num and num['state']}")
            n = len(S()["active"]["sets"])
            await ws.service("training_assistant", "next")  # ohne Werte → übernimmt Plus/Minus
            await wait_for(lambda: len(S()["active"]["sets"]) > n)
            rec = S()["active"]["sets"][-1]
            check(rec["exercise"] == step["exercise"] and rec["reps"] == adj["reps"] and rec["status"] == "corrected",
                  f"„Weiter“ übernimmt Plus/Minus: {rec['reps']} × {rec['weight_kg']} ({rec['status']})")
            await ws.service("training_assistant", "undo")  # Verlauf für spätere Prüfungen unverändert lassen
            await wait_for(lambda: len(S()["active"]["sets"]) == n)

            # Entitäten
            states = {s["entity_id"]: s for s in (await ws.call(type="get_states"))["result"]
                      if "trainingassistant" in s["entity_id"]}
            status = next((s for k, s in states.items() if k.startswith("sensor.") and k.endswith("status")), None)
            check(status is not None and status["state"] == "active", f"Status-Sensor = {status and status['state']}")
            check(len([k for k in states if k.startswith("button.")]) == 13, "13 Tasten vorhanden")

            await ws.service("training_assistant", "finish")
            await wait_for(lambda: S()["active"] is None)
            check(S()["next"]["workout_id"] == "b", "nach Beenden ist Workout B vorgemerkt")
            await ws.call(type="training_assistant/set_program", plan_id="feature_testplan")
            await wait_for(lambda: S()["program"] == "feature_testplan")
            await ws.call(type="training_assistant/set_program", plan_id="ganzkoerper_hypertrophie")
            await wait_for(lambda: S()["program"] == "ganzkoerper_hypertrophie")
            check(S()["next"]["workout_id"] == "b", "Programm gewechselt und zurück: Position (B) bleibt erhalten")

            log = (await ws.service("fake_voice", "get_log", response=True))["result"]["response"]["log"]
            asks = [x[2] for x in log if x[0] == "ask"]
            check(any(V["planned"] in q for q in asks), f"Rückfragen gestellt, z. B. „{asks[0] if asks else ''}“")
            check(any(V["finished"] in x[2] for x in log if x[0] == "announce"), "Abschlussansage")

            print("Verlauf und Vorschläge")
            hist = (await ws.call(type="training_assistant/history"))["result"]
            check(len(hist["sessions"]) >= 1, "Training im Verlauf")
            goblet = next((e for e in hist["exercises"] if e["exercise"] == "goblet_squat"), None)
            check(goblet is not None and goblet["suggestion"] is not None, "Vorschlag für Goblet Squats")
            prev = (await ws.call(type="training_assistant/preview", plan_id="ganzkoerper_hypertrophie",
                                  workout_id="a"))["result"]["steps"]
            g = next(s for s in prev if s.get("exercise") == "goblet_squat")
            check(g["target_weight"] == 16 and g["target_reps"] == 9,
                  f"Nächstes Ziel Goblet Squats: {g['target_reps']} × {g['target_weight']} kg ({g['suggestion']})")

            print("Personen, Anstrengung, Pausentimer, Rekorde, Statistik")
            res = await ws.call(type="training_assistant/stats")
            check(res["success"] and len(res["result"]["week"]["days"]) == 7, "Statistik: Woche mit 7 Tagen")
            home = S()["profile"]
            home_sessions = len((await ws.call(type="training_assistant/history"))["result"]["sessions"])
            res = await ws.call(type="training_assistant/profile", action="add", name="E2E Gast")
            guest = res["result"]["id"] if res["success"] else None
            check(guest is not None, "Person angelegt")
            bad = await ws.call(type="training_assistant/profile", action="add", name="e2e gast")
            check(not bad["success"], "doppelter Name abgelehnt")
            me = (await ws.call(type="auth/current_user"))["result"]["id"]
            users = (await ws.call(type="training_assistant/ha_users"))["result"]["users"]
            check(any(u["id"] == me for u in users), f"{len(users)} HA-Benutzer zum Verknüpfen")
            res = await ws.call(type="training_assistant/link_profile", profile=guest, user_id=me)
            await wait_for(lambda: any(x.get("user_id") == me for x in S()["profiles"]))
            check(res["success"] and next(x for x in S()["profiles"] if x["id"] == guest).get("user_id") == me,
                  "Person mit HA-Benutzer verknüpft")
            bad = await ws.call(type="training_assistant/link_profile", profile=guest, user_id="gibt_es_nicht")
            check(not bad["success"], "unbekannter Benutzer abgelehnt")
            await ws.call(type="training_assistant/link_profile", profile=guest, user_id=None)
            await wait_for(lambda: not any(x.get("user_id") for x in S()["profiles"]))
            check(not any(x.get("user_id") for x in S()["profiles"]), "Verknüpfung gelöst")
            await ws.call(type="training_assistant/profile", action="select", profile=guest)
            await wait_for(lambda: S()["profile"] == guest)
            hist = (await ws.call(type="training_assistant/history"))["result"]
            check(S()["profile"] == guest and not hist["sessions"], "Person gewechselt: eigener, leerer Verlauf")

            async def first_set(effort_text=None):
                await ws.service("training_assistant", "start", {"plan_id": "ganzkoerper_hypertrophie", "workout_id": "a"})
                await wait_for(lambda: S()["active"] is not None)
                await ws.service("training_assistant", "next")  # Aufwärmen fertig
                await wait_for(lambda: S()["active"]["phase"] == "ready")
                await ws.service("training_assistant", "next")  # los
                await wait_for(lambda: S()["active"]["phase"] == "active")
                return S()["active"]["steps"][S()["active"]["idx"]]

            step = await first_set()
            await ws.service("training_assistant", "next")
            await wait_for(lambda: len(S()["active"]["sets"]) == 1)
            await ws.service("training_assistant", "log_set", {"text": V["effort"]})
            await wait_for(lambda: S()["active"]["sets"][0].get("effort") == "hard")
            rec = S()["active"]["sets"][0]
            check(rec.get("effort") == "hard" and rec["reps"] == 8, f"„{V['effort']}“: {rec['reps']} Wdh., {rec.get('effort')}")
            res = await ws.call(type="training_assistant/edit_set", set_id=rec["id"], effort="easy")
            check(res["success"] and res["result"]["effort"] == "easy" and res["result"]["status"] == rec["status"],
                  "Anstrengung an der Karte geändert, Status bleibt")
            await ws.service("training_assistant", "rest_adjust", {"seconds": 15})
            await wait_for(lambda: S()["active"]["rest_until"] is not None)
            first = S()["active"]["rest_until"]
            await ws.service("training_assistant", "rest_adjust", {"seconds": 15})
            await wait_for(lambda: S()["active"]["rest_until"] != first)
            check(S()["active"]["rest_until"] > first, "Pause +15 s verlängert")
            await ws.service("training_assistant", "rest_adjust", {"seconds": -300})
            await wait_for(lambda: S()["active"]["rest_until"] is None)
            check(S()["active"]["rest_until"] is None, "Pause −15 s bis auf null beendet")
            bad = await ws.call(type="training_assistant/profile", action="select", profile=home)
            check(not bad["success"], "Personenwechsel während des Trainings abgelehnt")
            await ws.service("training_assistant", "finish")
            await wait_for(lambda: S()["active"] is None)

            step = await first_set()
            if step.get("target_weight") is not None:
                await ws.service("training_assistant", "next", {"weight_kg": step["target_weight"] + 10})
            else:
                await ws.service("training_assistant", "next", {"reps": (step.get("target_reps") or 8) + 10})
            await wait_for(lambda: S()["active"]["sets"] and S()["active"]["sets"][0].get("record"))
            check(bool(S()["active"]["sets"][0].get("record")), f"Rekord erkannt: {S()['active']['sets'][0].get('record')}")
            await ws.service("training_assistant", "finish")
            await wait_for(lambda: S()["active"] is None)
            res = (await ws.call(type="training_assistant/stats"))["result"]
            check(res["week"]["done"] == 2 and res["records"], f"Statistik der Person: {res['week']['done']} Trainings, "
                  f"{len(res['records'])} Rekord(e)")

            await ws.call(type="training_assistant/profile", action="select", profile=home)
            await wait_for(lambda: S()["profile"] == home)
            hist = (await ws.call(type="training_assistant/history"))["result"]
            check(len(hist["sessions"]) == home_sessions, "zurück: eigener Verlauf unverändert")
            res = await ws.call(type="training_assistant/profile", action="delete", profile=guest)
            await wait_for(lambda: guest not in [x["id"] for x in S()["profiles"]])
            check(res["success"] and guest not in [x["id"] for x in S()["profiles"]], "Person gelöscht")

            print("Offene Blöcke und HIIT (stumm, ohne Satellit)")
            await ws.service("training_assistant", "start", {"plan_id": "e2e_test", "workout_id": "t"})
            await wait_for(lambda: S()["active"] is not None)
            await ws.service("training_assistant", "next")  # Zirkel starten (3 s Zeitlimit)
            await wait_for(lambda: S()["active"].get("block_until") is not None)
            check(S()["active"].get("block_until") is not None, "Zeitlimit läuft")
            await ws.service("training_assistant", "next")
            await wait_for(lambda: S()["active"].get("block_expired"), 6)
            check(S()["active"]["block_expired"], "Zeitlimit abgelaufen")
            await ws.service("training_assistant", "next")
            await wait_for(lambda: S()["active"]["steps"][S()["active"]["idx"]].get("exercise") == "p")
            check(S()["active"]["steps"][S()["active"]["idx"]]["exercise"] == "p", "nach Zeitlimit: nächster Block")
            await ws.service("training_assistant", "next")  # bereit
            for reps in (6, 5):
                await ws.service("training_assistant", "next")
                await ws.service("training_assistant", "log_set", {"reps": reps})
            await wait_for(lambda: S()["active"]["steps"][S()["active"]["idx"]]["type"] == "interval")
            check(S()["active"]["steps"][S()["active"]["idx"]]["type"] == "interval", "10 Pull-Ups erreicht → HIIT")
            await ws.service("training_assistant", "next")  # HIIT starten
            await wait_for(lambda: S()["active"]["phase"] == "interval")
            check(S()["active"]["phase"] == "interval", "HIIT läuft")
            await wait_for(lambda: S()["active"]["steps"][S()["active"]["idx"]]["type"] == "cooldown", 8)
            check(S()["active"]["steps"][S()["active"]["idx"]]["type"] == "cooldown", "HIIT automatisch beendet")
            hiit_sets = [x for x in S()["active"]["sets"] if x["exercise"] == "h"]
            check(len(hiit_sets) == 2 and all(x["duration_s"] == 1 for x in hiit_sets),
                  f"HIIT-Intervalle als Sätze gespeichert ({len(hiit_sets)})")
            await ws.service("training_assistant", "next")
            await wait_for(lambda: S()["active"] is None)
            check(S()["active"] is None, "Training fertig")

            print("Aufräumen")
            await ws.call(type="training_assistant/delete_plan", plan_id="e2e_test")
            await ws.call(type="training_assistant/delete_plan", plan_id="feature_testplan")
            if previous_next and previous_next["plan_id"] != "e2e_test":
                await ws.call(type="training_assistant/set_next", **previous_next)
            await wait_for(lambda: all(p["id"] != "e2e_test" for p in S()["plans"]))
            check(all(p["id"] != "e2e_test" for p in S()["plans"]), "Testplan wieder entfernt")
            check(S()["next"] is None or S()["next"]["plan_id"] != "e2e_test", f"nächstes Workout: {S()['next']}")

            reader.cancel()
    print()
    print("ALLES OK" if not FAILED else f"{len(FAILED)} FEHLER")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
