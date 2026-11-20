"""Erzeugt die Vorlagen der Gruppe „Alltag & Gesundheit“ (alltag-*.yaml), die Woche für Woche wachsen.

Aufruf:  python3 tools/build_everyday_templates.py [--i18n <HU>/templates/i18n.yaml]
Schreibt custom_components/training_assistant/templates/alltag-1…3-*.yaml. Mit --i18n werden die deutschen
Übersetzungen aller neuen Texte in Hero Upgrades templates/i18n.yaml ergänzt (Abschnitt „Alltag & Gesundheit“).
Die Vorlagen sind Englisch; Hero Upgrade nutzt „Der lange Pfad“ und „Rückenschule“ zugleich als Story-Pläne.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "custom_components" / "training_assistant" / "templates"
DE: dict[str, str] = {}


def T(en: str, de: str) -> str:
    DE[en] = de
    return en


def q(s: str) -> str:
    """YAML-Text in doppelten Anführungszeichen (JSON-Strings sind gültiges YAML)."""
    return json.dumps(s, ensure_ascii=False)


def flow(obj) -> str:
    """Kleine Objekte in YAML-Flow-Schreibweise, Texte immer in Anführungszeichen."""
    if isinstance(obj, dict):
        return "{ " + ", ".join(f"{k}: {flow(v)}" for k, v in obj.items()) + " }"
    if isinstance(obj, list):
        return "[" + ", ".join(flow(v) for v in obj) + "]"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, str):
        return q(obj)
    return str(obj)


def block_yaml(b: dict) -> str:
    """Ein Block als YAML (Listenpunkt unter blocks:)."""
    lines, first = [], True
    for k, v in b.items():
        pre = "      - " if first else "        "
        first = False
        if k == "exercises" and isinstance(v, list) and v and isinstance(v[0], dict):
            lines.append(f"{pre}exercises:")
            lines += [f"          - {flow(e)}" for e in v]
        else:
            lines.append(f"{pre}{k}: {flow(v)}")
    return "\n".join(lines)


def write(file: str, header: str, name: str, description: str, goal: str, defaults: dict | None, exercises: str, workouts: list[dict]) -> None:
    out = [header.rstrip(), "schema_version: 1", f"name: {name}", "description: >-"]
    out += [f"  {line}" for line in description.split("\n")]
    out.append(f"goal: {goal}")
    if defaults:
        out.append("defaults:")
        out += [f"  {k}: {flow(v)}" for k, v in defaults.items()]
    out += ["exercises:", exercises.rstrip(), "workouts:"]
    for w in workouts:
        out += [f"  - id: {w['id']}", f"    name: {q(w['name'])}", "    blocks:"]
        out += [block_yaml(b) for b in w["blocks"]]
    (OUT / file).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{file}: {len(workouts)} Workouts")


def desc(en: str, de: str) -> str:
    """Beschreibung: einzeilig übersetzt (YAML faltet die Zeilen mit >- zu einer)."""
    T(" ".join(en.split()), de)
    return en


# ---------------------------------------------------------------------------------------------------------------
# 1 Gehen jeden Tag – 6 Wochen, 5 Spaziergänge pro Woche, von 15 auf 45 Minuten (WHO: 150 Minuten pro Woche).
WALK_MIN = [15, 20, 25, 30, 40, 45]
walks = []
for w, minutes in enumerate(WALK_MIN, 1):
    for d in range(1, 6):
        walks.append({"id": f"w{w}d{d}", "name": T(f"Week {w} · Walk {d}", f"Woche {w} · Spaziergang {d}"), "blocks": [
            {"type": "flow", "name": T(f"{minutes} minutes", f"{minutes} Minuten"), "rest_s": 0,
             "note": T("Start and finish easy; in between walk briskly – a little out of breath, but still able to talk.",
                       "Locker beginnen und ausklingen; dazwischen zügig gehen – etwas außer Atem, aber noch im Gespräch."),
             "exercises": [{"exercise": "walk", "duration_s": 300}, {"exercise": "brisk_walk", "duration_s": (minutes - 10) * 60},
                           {"exercise": "walk", "duration_s": 300}]}]})
write("alltag-1-gehen-taeglich.yaml",
      """# Template: daily walking – from 15 to 45 minutes a day in 6 weeks, five days a week.
# Inspired by the WHO recommendation of at least 150 minutes of moderate activity per week; brisk walking counts.
# Every walk starts and ends with five easy minutes. Timed – runs on its own.""",
      T("Daily Walking 6 Weeks", "Jeden Tag gehen 6 Wochen"),
      desc("""Walking as training: 6 weeks, 5 walks per week, from 15 to 45 minutes. Five easy minutes at the start and
end, brisk walking in between. In week 4 you reach the 150 minutes per week the WHO recommends.
No equipment – good shoes are enough.""",
           "Gehen als Training: 6 Wochen, 5 Spaziergänge pro Woche, von 15 auf 45 Minuten. Fünf lockere Minuten am Anfang und Ende, dazwischen zügig gehen. In Woche 4 erreichst du die 150 Minuten pro Woche, die die WHO empfiehlt. Ohne Geräte – gute Schuhe genügen."),
      "endurance", None,
      """  walk: { name: Walk, aliases: [Gehen, Spazieren], equipment: other, image: Walking_Treadmill, muscles: [] }
  brisk_walk: { name: Brisk Walk, aliases: [Zügiges Gehen], equipment: other, image: Walking_Treadmill, muscles: [] }""",
      walks)

# ---------------------------------------------------------------------------------------------------------------
# 2 Fit fürs Wandern – 8 Wochen, 3× pro Woche: Kraft für Berg und Treppe, Treppen-Intervalle, eine lange Wanderung,
# die von 1 auf 4 Stunden wächst. Ziel: eine Tagestour oder die erste Etappe einer Mehrtageswanderung.
T("Hike", "Wandern")  # Übungsname
HIKE_MIN = [60, 75, 90, 105, 120, 150, 180, 240]
STAIRS = [(6, 60), (6, 75), (7, 90), (7, 90), (8, 105), (8, 120), (8, 120), (6, 90)]
hikes = []
for w in range(1, 9):
    rounds = 2 if w <= 3 else 3
    hikes.append({"id": f"w{w}a", "name": T(f"Week {w} · Strength", f"Woche {w} · Kraft"), "blocks": [
        {"type": "warmup", "duration_s": 300, "note": T("Five minutes of brisk walking or marching on the spot.", "Fünf Minuten zügig gehen oder auf der Stelle marschieren.")},
        {"type": "circuit", "name": T("Legs for the mountain", "Beine für den Berg"), "rounds": rounds,
         "rest_after_exercise_s": 15, "rest_after_round_s": 60,
         "note": T("Slow and controlled. Step-ups: push through the heel of the upper foot.", "Langsam und kontrolliert. Step-ups: über die Ferse des oberen Fußes hochdrücken."),
         "exercises": [{"exercise": "step_up", "reps": {"min": 10, "max": 15}, "per_side": True},
                       {"exercise": "reverse_lunge", "reps": {"min": 8, "max": 12}, "per_side": True},
                       {"exercise": "calf_raise", "reps": {"min": 15, "max": 25}},
                       {"exercise": "glute_bridge", "reps": {"min": 12, "max": 20}},
                       {"exercise": "side_plank", "duration_s": 20 + 5 * min(w, 4), "per_side": True}]},
        {"type": "cooldown"}]})
    r, s = STAIRS[w - 1]
    hikes.append({"id": f"w{w}b", "name": T(f"Week {w} · Stairs", f"Woche {w} · Treppe"), "blocks": [
        {"type": "warmup", "duration_s": 300, "note": T("Five minutes of brisk walking.", "Fünf Minuten zügig gehen.")},
        {"type": "interval", "name": T(f"{r} × stairs", f"{r} × Treppe"), "rounds": r, "work_s": s, "rest_s": 60,
         "note": T("Climb briskly, walk back down calmly in the rest. A hill works just as well.", "Zügig hinauf, in der Pause ruhig wieder hinunter. Ein Hügel geht genauso."),
         "exercises": ["stair_climb"]},
        {"type": "cooldown", "duration_s": 300}]})
    m = HIKE_MIN[w - 1]
    label = T(f"{m // 60} hours", f"{m // 60} Stunden") if m % 60 == 0 and m > 60 else T(f"{m} minutes", f"{m} Minuten")
    last = w == 8
    hikes.append({"id": f"w{w}c", "name": T("Week 8 · Tour day", "Woche 8 · Tourentag") if last else T(f"Week {w} · Long hike", f"Woche {w} · Lange Wanderung"), "blocks": [
        {"type": "flow", "name": label, "rest_s": 0,
         "note": T("The tour day: four hours with a day pack, ups and downs. Breaks are part of it – pause the timer for them.",
                   "Der Tourentag: vier Stunden mit Tagesrucksack, bergauf und bergab. Pausen gehören dazu – dafür den Timer anhalten.") if last
         else T("Steady pace with a day pack (3–5 kg), hills wherever you can find them. Drink regularly.",
                "Gleichmäßiges Tempo mit Tagesrucksack (3–5 kg), Steigungen, wo immer du welche findest. Regelmäßig trinken."),
         "exercises": [{"exercise": "hike", "duration_s": m * 60}]}]})
write("alltag-2-wandern.yaml",
      """# Template: hiking fitness – 8 weeks toward a four-hour mountain day or the first stage of a multi-day hike.
# Three sessions a week: leg strength for climbing and descending, stair intervals, and one long hike that grows
# from one to four hours. Own program after common hike-training advice (alpine clubs, trail guides).""",
      T("Hiking Fitness 8 Weeks", "Fit fürs Wandern 8 Wochen"),
      desc("""Fit for the mountains: 8 weeks, 3 sessions per week. Leg strength for climbing and descending
(step-ups, lunges, calf raises, glute bridge, side plank), stair intervals, and one long hike that grows
from one to four hours. The last week ends with a tour day. A chair, a staircase and a day pack.""",
           "Fit für die Berge: 8 Wochen, 3 Einheiten pro Woche. Beinkraft für bergauf und bergab (Step-ups, Ausfallschritte, Wadenheben, Glute Bridge, Seitstütz), Treppen-Intervalle und eine lange Wanderung, die von einer auf vier Stunden wächst. Die letzte Woche endet mit einem Tourentag. Ein Stuhl, eine Treppe und ein Tagesrucksack."),
      "endurance", {"rest_s": 60, "progression": {"type": "reps"}},
      """  hike: { name: Hike, aliases: [Wandern, Wanderung], equipment: other, image: Walking_Treadmill, muscles: [quads, glutes, calves] }
  stair_climb: { name: Stair Climbing (brisk), aliases: [Treppensteigen zügig], equipment: bodyweight, image: Stairmaster,
                 muscles: [quads, glutes, calves] }
  step_up: { name: Step-up onto Chair, aliases: [Aufsteigen auf Stuhl], equipment: bodyweight, image: Dumbbell_Step_Ups, unilateral: true }
  reverse_lunge: { name: Reverse Lunge, aliases: [Ausfallschritt rückwärts], equipment: bodyweight, image: Crossover_Reverse_Lunge, unilateral: true }
  calf_raise: { name: Calf Raise, aliases: [Wadenheben], equipment: bodyweight, image: Standing_Calf_Raises }
  glute_bridge: { name: Glute Bridge, aliases: [Hüftheben], equipment: bodyweight, image: Butt_Lift_Bridge }
  side_plank: { name: Side Plank, aliases: [Seitstütz], equipment: bodyweight, image: Side_Bridge, unilateral: true }""",
      hikes)

# ---------------------------------------------------------------------------------------------------------------
# 3 Rückenschule – 8 Wochen, 2× pro Woche. Angelehnt an die „Neue Rückenschule“ (KddR): Bewegung, Mobilisation,
# Rumpfkraft, rückengerechtes Heben, Entspannung. Drei Abschnitte: sanft (Woche 1–2), aufbauen (3–5), kräftigen (6–8).
backs = []
for i in range(16):
    w = i // 2 + 1
    ph = 0 if w <= 2 else 1 if w <= 5 else 2
    reps = [6, 8, 10][ph]
    strength = [{"exercise": "curl_up", "reps": reps}, {"exercise": "bird_dog", "reps": reps, "per_side": True},
                {"exercise": "side_plank", "duration_s": [15, 25, 35][ph], "per_side": True},
                {"exercise": "glute_bridge", "reps": [10, 12, 15][ph]}]
    if ph >= 1:
        strength.append({"exercise": "dead_bug", "reps": [8, 8, 10][ph], "per_side": True})
    if ph == 2:
        strength.append({"exercise": "superman", "reps": 10})
    backs.append({"id": f"s{i + 1:02d}", "name": T(f"Week {w} · Session {i % 2 + 1}", f"Woche {w} · Einheit {i % 2 + 1}"), "blocks": [
        {"type": "flow", "name": T("Walk in", "Eingehen"), "rest_s": 0,
         "note": T("Five minutes of brisk walking – outside or through the flat.", "Fünf Minuten zügig gehen – draußen oder durch die Wohnung."),
         "exercises": [{"exercise": "brisk_walk", "duration_s": 300}]},
        {"type": "flow", "name": T("Mobilise", "Mobilisieren"), "rest_s": 5,
         "note": T("Slow, small movements without pain. Breathe calmly.", "Langsame, kleine Bewegungen ohne Schmerz. Ruhig atmen."),
         "exercises": [{"exercise": "cat_cow", "duration_s": 60}, {"exercise": "pelvic_tilt", "duration_s": 60},
                       {"exercise": "knee_to_chest", "duration_s": 30, "per_side": True}, {"exercise": "supine_twist", "duration_s": 30, "per_side": True},
                       {"exercise": "child_pose", "duration_s": 60}]},
        {"type": "circuit", "name": T("Strong trunk", "Starker Rumpf"), "rounds": [2, 3, 3][ph], "rest_after_exercise_s": 15, "rest_after_round_s": 60,
         "note": T("Hold every rep of curl-up and bird dog for about 10 seconds. Keep the back in its natural curve.",
                   "Jede Wiederholung von Curl-up und Bird Dog etwa 10 Sekunden halten. Den Rücken in seiner natürlichen Form lassen."),
         "exercises": strength},
        {"type": "sets", "exercise": "db_romanian_deadlift", "sets": [2, 2, 3][ph], "reps": 10, "weight_kg": [2, 4, 6][ph], "rest_s": 60,
         "note": T("Lifting the right way: bend at the hips, back long, weight close to the body. Two water bottles are enough at the start.",
                   "Richtig heben: aus der Hüfte beugen, Rücken lang, Gewicht nah am Körper. Zwei Wasserflaschen genügen am Anfang.")},
        {"type": "flow", "name": T("Relax", "Entspannen"), "rest_s": 0,
         "note": T("Lie on your back. Tense one body part after another for five seconds, then let go completely.",
                   "Auf dem Rücken liegen. Nacheinander jede Körperpartie fünf Sekunden anspannen, dann ganz loslassen."),
         "exercises": [{"exercise": "savasana", "duration_s": [180, 240, 300][ph]}]}]})
write("alltag-3-rueckenschule.yaml",
      """# Template: back school – 8 weeks, twice a week, about 30 minutes.
# Inspired by the German "Neue Rückenschule" (KddR), the standard for back courses of the health insurers:
# move, mobilise, strengthen the trunk, learn to lift, relax. Three stages: gentle (weeks 1-2), building (3-5),
# stronger (6-8). Not a therapy – with acute pain or radiating pain see a doctor first.""",
      T("Back School 8 Weeks", "Rückenschule 8 Wochen"),
      desc("""A strong, mobile back for everyday life: 8 weeks, 2 sessions per week, about 30 minutes. Walk in,
mobilise gently, strengthen the trunk (curl-up, bird dog, side plank, glute bridge, dead bug), learn to lift
with a light weight, then relax. Three stages from gentle to stronger. Inspired by the German
"Neue Rückenschule". With acute or radiating pain see a doctor first.""",
           "Ein starker, beweglicher Rücken für den Alltag: 8 Wochen, 2 Einheiten pro Woche, etwa 30 Minuten. Eingehen, sanft mobilisieren, den Rumpf kräftigen (Curl-up, Bird Dog, Seitstütz, Glute Bridge, Dead Bug), mit leichtem Gewicht richtig heben lernen, dann entspannen. Drei Abschnitte von sanft bis kräftigend. Angelehnt an die „Neue Rückenschule“. Bei akuten oder ausstrahlenden Schmerzen erst zum Arzt."),
      "general", {"rest_s": 30, "progression": {"type": "none"}},
      """  brisk_walk: { name: Brisk Walk, aliases: [Zügiges Gehen], equipment: other, image: Walking_Treadmill, muscles: [] }
  cat_cow: { name: Cat-Cow, aliases: [Katze-Kuh], equipment: bodyweight, image: Cat_Stretch }
  pelvic_tilt: { name: Pelvic Tilt, aliases: [Beckenkippen], equipment: bodyweight, image: Pelvic_Tilt_Into_Bridge }
  knee_to_chest: { name: Knee to Chest, aliases: [Knie zur Brust], equipment: bodyweight, image: One_Knee_To_Chest }
  supine_twist: { name: Supine Twist, aliases: [Liegender Drehsitz], equipment: bodyweight, image: Lying_Crossover, unilateral: true }
  child_pose: { name: Child's Pose, aliases: [Kind], equipment: bodyweight, image: Childs_Pose }
  curl_up: { name: McGill Curl-Up, aliases: [Curl-up], equipment: bodyweight, image: false, muscles: [core],
             note: "One leg bent, hands under the lower back. Lift head and shoulders only slightly." }
  bird_dog: { name: Bird Dog, aliases: [Vierfüßlerstand diagonal], equipment: bodyweight, image: false,
              muscles: [core, glutes, back], unilateral: true }
  side_plank: { name: Side Plank, aliases: [Seitstütz], equipment: bodyweight, image: Side_Bridge, unilateral: true }
  glute_bridge: { name: Glute Bridge, aliases: [Hüftheben], equipment: bodyweight, image: Butt_Lift_Bridge }
  dead_bug: { name: Dead Bug, equipment: bodyweight, unilateral: true }
  superman: { name: Superman, aliases: [Rückenstrecker liegend], equipment: bodyweight, image: Superman }
  db_romanian_deadlift: { name: Dumbbell Romanian Deadlift, aliases: [Rumänisches Kreuzheben Kurzhantel], equipment: dumbbell, image: Stiff-Legged_Dumbbell_Deadlift }
  savasana: { name: Final Relaxation, aliases: [Endentspannung, Savasana], equipment: bodyweight, image: false, muscles: [] }""",
      backs)

if "--i18n" in sys.argv:
    path = Path(sys.argv[sys.argv.index("--i18n") + 1])
    text = path.read_text(encoding="utf-8")
    mark = "  # -- Alltag & Gesundheit (tools/build_everyday_templates.py in TrainingAssistant) --"
    if mark in text:  # alten Abschnitt ersetzen
        text = text[:text.index(mark)].rstrip("\n") + "\n"
    import re
    have = set(re.findall(r'^  ("(?:[^"\\]|\\.)*"):', text, re.M))
    new = [f"  {q(en)}: {q(de)}" for en, de in DE.items() if q(en) not in have]
    path.write_text(text.rstrip("\n") + "\n" + mark + "\n" + "\n".join(new) + "\n", encoding="utf-8")
    print(f"{len(new)} Übersetzungen → {path}")
