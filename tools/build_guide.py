"""Erzeugt die Nutzer-Anleitungen in custom_components/training_assistant/guide/:

  guide-custom-plans.txt      (Englisch, Prompt aus docs/plan-format.md, Beispiel example-plan.yaml)
  anleitung-eigene-plaene.txt (Deutsch, Prompt aus docs/plan-format.de.md, Beispiel beispiel-plan.yaml)

So bleibt alles an einer Stelle gepflegt. Nach Änderungen an Format/Doku/Beispiel ausführen:

    .venv/bin/python tools/build_guide.py

tests/test_guide.py prüft, dass die Dateien aktuell sind.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
GUIDE_DIR = ROOT / "custom_components" / "training_assistant" / "guide"

LINE = "=" * 78

INTRO_EN = f"""{LINE}
  TrainingAssistant – Creating and importing your own training plans
{LINE}

A training plan is a text file in YAML (or JSON) format. It describes your
exercises and workouts. You paste the text into the TrainingAssistant card:

    Tab "Settings" → "Own plan" → paste the text → "Import"

If something is wrong, the card shows exactly where (e.g.
"workouts/0/blocks/2/exercise: exercise 'squats' is not in the 'exercises' catalog").
A plan with the same name is replaced – your history is kept.


{LINE}
  1. Three ways to your own plan
{LINE}

A) Adapt a template (easiest)
   Tab "Settings" → "Templates" → add a template → under "My plans", click "Edit".
   The text then appears in the import field. Change it (e.g. weights,
   exercises, names) and press "Import".

B) Let ChatGPT, Claude or similar create it
   Copy the prompt from section 4, fill in your wishes at the bottom (goal,
   days per week, equipment, starting weights) – or attach an existing plan
   (table, photo, PDF) and write "Convert the attached plan".
   Paste the answer (only the YAML text) into the import field.

C) Write it yourself
   Start with the example from section 5 – it is already in the card's import
   field – and adapt it.


{LINE}
  2. Structure of a plan
{LINE}

  schema_version: 1        always 1
  name                     name of the plan
  description              (optional) short description
  defaults                 (optional) rest and progression for all exercises
  exercises                exercise catalog: ID → name, equipment, (image, muscles)
  workouts                 workouts, suggested in rotation
    └ blocks               sections in a fixed order

  Block types:
    warmup / cooldown      warm-up / cool-down, end with the button
    sets                   sets of one exercise (e.g. 5×5, 3×8–12)
    circuit                circuit: all exercises one after another, several rounds
                           (rounds) or rounds until time is up (time_cap_s)
    interval               HIIT: work/rest in seconds, timed
    flow                   timed sequence, own duration per exercise (yoga)

  Values per set:
    reps                   8  ·  {{ min: 8, max: 12 }}  ·  max
    duration_s             instead of reps: 30  ·  {{ min: 30, max: 45 }}  ·  max
    weight_kg              weight; omit = bodyweight
    per_side: true         per arm/leg
    tempo: "3-0-1"         gets announced

  Rest (seconds):
    rest_s                 between sets (sets)
    rest_after_exercise_s  between exercises in a circuit
    rest_after_round_s     between circuit rounds
    rest_after_s           after the whole block

  Progression (suggestions for the next session):
    {{ type: double, increment_kg: 2.5 }}   first reps up to the upper limit, then +weight
                                         (needs reps: {{ min, max }})
    {{ type: linear, increment_kg: 2.5 }}   all sets done → +weight (e.g. 5×5)
    {{ type: reps, max_reps: 20 }}          bodyweight: +1 rep per session
    {{ type: none }}                        no suggestions

  Images: found automatically via the English or German exercise name.
  Set them yourself with image: <image name> (e.g. Goblet_Squat) or
  image: false for no image.

  Muscle groups (for "sets per muscle group" and recovery): automatic via the
  exercise name, or set them yourself, e.g. muscles: [hamstrings, glutes, back].
  Groups: chest, back, shoulders, biceps, triceps, core, quads, hamstrings,
  glutes, calves. muscles: [] = whole body, not counted.


{LINE}
  3. Common mistakes
{LINE}

  - Indentation: spaces only, no tabs. Same level = same indentation.
  - Commas in the short notation {{ … }}: put text with a comma in quotes,
    e.g.  note: "Slow, controlled"
  - Also put text containing a colon followed by a space in quotes.
  - Every exercise used in a block must be listed under exercises.
  - Don't combine a fixed rep count (reps: 8) with type: double –
    use linear, reps or none there.
  - Never use reps and duration_s at the same time.


{LINE}
  4. Prompt for ChatGPT, Claude & co.
{LINE}

"""

EXAMPLE_HEAD_EN = f"""

{LINE}
  5. Example plan
{LINE}

"""

INTRO_DE = f"""{LINE}
  TrainingAssistant – Eigene Trainingspläne anlegen und importieren
{LINE}

Ein Trainingsplan ist eine Textdatei im Format YAML (oder JSON). Sie beschreibt
deine Übungen und Workouts. Du fügst den Text in der TrainingAssistant-Karte ein:

    Reiter „Einstellungen“ → „Eigener Plan“ → Text einfügen → „Importieren“

Ist etwas falsch, zeigt die Karte genau an, wo (z. B.
„workouts/0/blocks/2/exercise: Übung 'kniebeuge' steht nicht im Katalog“).
Ein Plan mit gleichem Namen wird ersetzt – dein Verlauf bleibt erhalten.


{LINE}
  1. Drei Wege zum eigenen Plan
{LINE}

A) Vorlage anpassen (am einfachsten)
   Reiter „Einstellungen“ → „Vorlagen“ → eine Vorlage übernehmen → unter „Meine Pläne“ auf
   „Bearbeiten“. Der Text steht dann im Importfeld. Ändern (z. B. Gewichte,
   Übungen, Namen) und „Importieren“ drücken.

B) Mit ChatGPT, Claude o. Ä. erzeugen lassen
   Den Prompt aus Abschnitt 4 kopieren, unten deine Wünsche eintragen (Ziel,
   Tage pro Woche, Ausrüstung, Startgewichte) – oder einen vorhandenen Plan
   (Tabelle, Foto, PDF) anhängen und „Wandle den angehängten Plan um“ schreiben.
   Die Antwort (nur der YAML-Text) in das Importfeld einfügen.

C) Selbst schreiben
   Mit dem Beispiel aus Abschnitt 5 starten – es steht auch schon im Importfeld
   der Karte – und anpassen.


{LINE}
  2. Aufbau eines Plans
{LINE}

  schema_version: 1        immer 1
  name                     Name des Plans
  description              (optional) kurze Beschreibung
  defaults                 (optional) Pause und Progression für alle Übungen
  exercises                Übungskatalog: ID → Name, Ausrüstung, (Bild, Muskeln)
  workouts                 Workouts, werden reihum vorgeschlagen
    └ blocks               Abschnitte in fester Reihenfolge

  Blocktypen:
    warmup / cooldown      Aufwärmen / Cool Down, enden per Knopf
    sets                   Sätze einer Übung (z. B. 5×5, 3×8–12)
    circuit                Zirkel: alle Übungen nacheinander, mehrere Runden
                           (rounds) oder Runden bis die Zeit um ist (time_cap_s)
    interval               HIIT: Arbeit/Pause in Sekunden, zeitgesteuert
    flow                   zeitgesteuerte Abfolge, eigene Dauer je Übung (Yoga)

  Werte pro Satz:
    reps                   8  ·  {{ min: 8, max: 12 }}  ·  max
    duration_s             statt reps: 30  ·  {{ min: 30, max: 45 }}  ·  max
    weight_kg              Gewicht; weglassen = Körpergewicht
    per_side: true         pro Arm/Bein
    tempo: "3-0-1"         wird angesagt

  Pausen (Sekunden):
    rest_s                 zwischen Sätzen (sets)
    rest_after_exercise_s  zwischen Übungen im Zirkel
    rest_after_round_s     zwischen Zirkelrunden
    rest_after_s           nach dem ganzen Block

  Progression (Vorschläge fürs nächste Training):
    {{ type: double, increment_kg: 2.5 }}   erst Wdh. bis zur Obergrenze, dann +Gewicht
                                         (braucht reps: {{ min, max }})
    {{ type: linear, increment_kg: 2.5 }}   alle Sätze geschafft → +Gewicht (z. B. 5×5)
    {{ type: reps, max_reps: 20 }}          Körpergewicht: +1 Wdh. pro Training
    {{ type: none }}                        keine Vorschläge

  Bilder: werden über den englischen oder deutschen Übungsnamen automatisch
  gefunden. Selbst festlegen mit image: <Bildname> (z. B. Goblet_Squat) oder
  image: false für kein Bild.

  Muskelgruppen (für „Sätze pro Muskelgruppe“ und Erholung): automatisch über
  das Bild, oder selbst angeben, z. B. muscles: [hamstrings, glutes, back].
  Gruppen: chest, back, shoulders, biceps, triceps, core, quads, hamstrings,
  glutes, calves. muscles: [] = Ganzkörper, wird nicht gezählt.


{LINE}
  3. Häufige Fehler
{LINE}

  - Einrückung: nur Leerzeichen, keine Tabulatoren. Gleiche Ebene = gleiche
    Einrückung.
  - Kommas in der Kurzschreibweise {{ … }}: Text mit Komma in Anführungszeichen,
    z. B.  note: "Langsam, kontrolliert"
  - Doppelpunkt mit Leerzeichen im Text ebenfalls in Anführungszeichen.
  - Jede Übung, die in einem Block vorkommt, muss unter exercises stehen.
  - Feste Wiederholungszahl (reps: 8) nicht mit type: double kombinieren –
    dort linear, reps oder none nehmen.
  - reps und duration_s nie gleichzeitig.


{LINE}
  4. Prompt für ChatGPT, Claude & Co.
{LINE}

"""

EXAMPLE_HEAD_DE = f"""

{LINE}
  5. Beispielplan
{LINE}

"""



LANGS = {
    "en": (ROOT / "docs" / "plan-format.md", GUIDE_DIR / "example-plan.yaml", GUIDE_DIR / "guide-custom-plans.txt",
           INTRO_EN, EXAMPLE_HEAD_EN),
    "de": (ROOT / "docs" / "plan-format.de.md", GUIDE_DIR / "beispiel-plan.yaml", GUIDE_DIR / "anleitung-eigene-plaene.txt",
           INTRO_DE, EXAMPLE_HEAD_DE),
}


def build(lang: str = "en") -> str:
    doc_path, example, _, intro, example_head = LANGS[lang]
    doc = doc_path.read_text(encoding="utf-8")
    match = re.search(r"````text\n(.*?)````", doc, re.S)
    if not match:
        raise SystemExit(f"Prompt-Block (````text … ````) in {doc_path.name} nicht gefunden")
    prompt = match.group(1).rstrip() + "\n"
    return intro + prompt + example_head + example.read_text(encoding="utf-8")


def main() -> int:
    for lang, (*_, target, _intro, _head) in LANGS.items():
        target.write_text(build(lang), encoding="utf-8")
        print(f"geschrieben: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
