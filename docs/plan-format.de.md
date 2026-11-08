# Importformat für Trainingspläne (Version 1)

*English version: [plan-format.md](plan-format.md)*

Ein Plan ist eine YAML- oder JSON-Datei. Die genaue Definition steht in
[`schema/plan.schema.json`](../schema/plan.schema.json). Vollständige Beispiele:
[`examples/ganzkoerper.yaml`](../examples/ganzkoerper.yaml) (alle Blocktypen) und
[`tests/fixtures/feature-testplan.yaml`](../tests/fixtures/feature-testplan.yaml) (Zirkeltraining mit
max-Sätzen, „pro Seite“ und Sätzen bis zu einer Gesamtzahl).

Importiert wird in der Dashboard-Karte (Reiter **Einstellungen** → **Eigener Plan** → einfügen → *Importieren*) oder
mit der Aktion `training_assistant.import_plan`. Ein Plan mit gleichem `name` wird ersetzt,
der Verlauf bleibt erhalten.

## Aufbau

```
Plan
├── exercises   Übungskatalog (ID → Name, Aliase, Equipment)
└── workouts    Trainingseinheiten (z. B. Workout 1–4), werden reihum vorgeschlagen
    └── blocks  Abschnitte in fester Reihenfolge
```

**Übungs-IDs** (`goblet_squat`) sind wichtig: Darüber ordnet die Integration den Verlauf zu,
auch über verschiedene Pläne hinweg. Eine Übung sollte also in jedem Plan dieselbe ID haben.

## Übungsbilder

Die Karte zeigt zu jeder Übung Fotos (Start- und Endposition) aus
[free-exercise-db](https://github.com/yuhonas/free-exercise-db) (gemeinfrei, über 870 Übungen).
Beim Import lädt Home Assistant nur die Bilder der Übungen im Plan einmal herunter. Danach
kommen sie lokal von Home Assistant.

Die Zuordnung passiert automatisch über `name`, `aliases` und die Übungs-ID. Gängige deutsche
Namen wie „Kreuzheben“ oder „Klimmzüge“ werden erkannt. Die Karte zeigt beim Import, welche
Übungen kein Bild bekommen haben. Selbst zuordnen kannst du so:

```yaml
exercises:
  javelin_press:
    name: Javelin Press
    image: Dumbbell_Shoulder_Press   # Ordnername aus free-exercise-db/exercises
  burpee:
    name: Burpees
    image: false                     # bewusst kein Bild
```

Die Bild-IDs findest du auf der [Katalogseite](https://yuhonas.github.io/free-exercise-db/)
(Übung öffnen, ID in der Adresse) oder im Ordner
[exercises](https://github.com/yuhonas/free-exercise-db/tree/main/exercises).

## Muskelgruppen

Sätze pro Muskelgruppe und der Erholungsstatus nutzen die Muskeln des Katalogbilds. Du kannst sie selbst
angeben – das gilt immer vorrangig, z. B. für Übungen ohne Bild:

```yaml
exercises:
  trap_bar_deadlift:
    name: Trap Bar Deadlift
    muscles: [quads, glutes, back]
  burpee:
    name: Burpees
    muscles: []        # Ganzkörper – bewusst keiner Muskelgruppe zugeordnet
```

Gruppen: `chest` (Brust), `back` (Rücken), `shoulders` (Schultern), `biceps`, `triceps`, `core` (Bauch),
`quads` (Oberschenkel vorn), `hamstrings` (Oberschenkel hinten), `glutes` (Po), `calves` (Waden).
Übungen ohne Bild und ohne `muscles` zeigt die Karte unter „Ohne Muskelgruppe“ an.

## Blocktypen

| Typ        | Wofür                                    | Felder                                                     |
|------------|------------------------------------------|------------------------------------------------------------|
| `warmup`   | Aufwärmen, endet per Knopf               | `name`, `duration_s`, `note`                               |
| `sets`     | Sätze einer Übung (5x5, 3x8–12)          | `exercise`, `sets` **oder** `total_reps`, Satz-Werte (s. u.), `rest_s`, `rest_after_s` |
| `circuit`  | Zirkel: alle Übungen je 1 Satz pro Runde | `rounds` **oder** `time_cap_s`, `exercises[]`, `rest_after_exercise_s`, `rest_after_round_s`, `rest_after_s`, `tempo` |
| `interval` | HIIT, rein zeitgesteuert                 | `rounds`, `work_s`, `rest_s`, `exercises[]` (IDs, reihum), `rest_after_s` |
| `cooldown` | Cool Down                                | wie `warmup`                                               |

Alle Blöcke können `name` und `note` haben. Die Notiz wird bei der Blockansage vorgelesen,
z. B. „Gewicht um 5–10 % erhöhen“.

### Offene Blöcke

- **Zirkel mit Zeitlimit** („die zwei Übungen 5 Minuten im Wechsel“): `time_cap_s: 300`
  statt `rounds`. Die Runden laufen weiter, bis die Zeit um ist. Danach beendest du die
  laufende Übung, und es geht mit dem nächsten Block weiter.
- **Sätze bis zur Gesamtzahl** („20 Pull-Ups, so viele Sätze wie nötig“): `total_reps: 20`
  statt `sets`, meist mit `reps: max`.

### Pausen

| Feld                    | Bedeutung                                          |
|-------------------------|----------------------------------------------------|
| `rest_s`                | (sets) Pause zwischen den Sätzen                   |
| `rest_after_exercise_s` | (circuit) Pause zwischen zwei Übungen einer Runde  |
| `rest_after_round_s`    | (circuit) Pause zwischen den Runden                |
| `rest_after_s`          | Pause nach dem ganzen Block („2 minutes break“)    |
| `defaults.rest_s`       | Standard, wo nichts anderes steht                  |

## Satz-Werte (bei `sets` und bei jeder Übung im `circuit`)

| Feld          | Werte                                                         |
|---------------|---------------------------------------------------------------|
| `reps`        | `8` · `{min: 8, max: 12}` · `max` (so viele wie möglich)      |
| `duration_s`  | `30` · `{min: 30, max: 45}` · `max` (so lange wie möglich halten) |
| `weight_kg`   | Zahl; weglassen = Körpergewicht                               |
| `per_side`    | `true` = Wiederholungen pro Arm/Bein                          |
| `tempo`       | z. B. `"3-0-1"`, wird angesagt                                |
| `progression` | siehe unten                                                   |
| `note`        | Hinweis, z. B. „in 45 Sekunden“                               |

`reps` und `duration_s` schließen sich aus: genau eins von beiden.

## Progression (Vorschläge fürs nächste Training)

| `type`   | Regel                                                                 |
|----------|-----------------------------------------------------------------------|
| `double` | Pro Training +1 Wdh. auf den schwächsten Satz. Alle Sätze am oberen Ende des Bereichs → `+increment_kg`, zurück aufs untere Ende. Braucht `reps: {min, max}`. |
| `linear` | Alle Sätze mit Zielwiederholungen geschafft → `+increment_kg` (z. B. 5x5). |
| `reps`   | Für Körpergewicht: Alle Sätze mit dem Ziel geschafft → nächstes Mal `+increment` Wdh. (Standard 1), bis `max_reps`. Danach Hinweis auf eine schwerere Variante. Ohne `max_reps` gilt das obere Ende eines Bereichs, bei fester Zahl unbegrenzt. |
| `none`   | Keine Vorschläge, feste Vorgabe aus dem Plan.                         |

`defaults.progression` gilt für alle Übungen, einzelne Übungen können das überschreiben.
Zeit-Sätze und `reps: max` laufen automatisch ohne Progression. Feste `reps` (z. B. `8`)
vertragen sich nicht mit `double`. Dort `linear` (mit Gewicht), `reps` (Körpergewicht)
oder `none` angeben.

Die Vorschläge werden beim Start eines Trainings zu den Zielwerten. Der Satellit fragt also
„10 mal 18 Kilo wie geplant?“, wenn letztes Mal alles geklappt hat.

## Plan prüfen

```bash
python tools/validate_plan.py mein-plan.yaml
```

Die Integration prüft beim Import genauso und meldet Fehler mit Pfad, z. B.
`workouts/0/blocks/2/exercises/1: Übung 'bench' steht nicht im Katalog`.

---

## Prompt für ein LLM

Den folgenden Text zusammen mit deinen Wünschen an ChatGPT, Claude o. Ä. geben.
Am besten hängst du `schema/plan.schema.json` als Datei an. Du kannst auch eine Tabelle,
ein Foto oder ein PDF mit einem bestehenden Trainingsplan anhängen und um Umwandlung bitten.

````text
Erstelle mir einen Trainingsplan im YAML-Format „TrainingAssistant Version 1“.
Halte dich exakt an diese Regeln und gib NUR den YAML-Code aus, ohne Erklärungen.

Oberste Ebene:
  schema_version: 1          (immer genau 1)
  name: <Text>
  description: <Text>        (optional)
  goal: hypertrophy | strength | endurance | general   (optional)
  defaults:                  (optional)
    rest_s: <Sekunden>
    progression: <Progression>
  exercises:                 Katalog, Schlüssel = ID in snake_case (a–z, 0–9, _)
    <id>:
      name: <Anzeigename>
      aliases: [<weitere Namen>]       (optional)
      equipment: bodyweight | dumbbell | kettlebell | barbell | band | machine | cable | other
      note: <Technik-Hinweis>          (optional)
      image: <Bild-ID aus free-exercise-db> (optional, sonst automatisch; false = kein Bild)
      muscles: [chest | back | shoulders | biceps | triceps | core | quads | hamstrings | glutes | calves]
                                       (optional, Hauptmuskeln; [] = Ganzkörper/keine)
  workouts:                  Liste
    - id: <snake_case>
      name: <Text>
      blocks: [<Block>, ...]

Block-Typen (Feld "type"), alle mit optional name und note:
  warmup / cooldown: duration_s?
  sets:     exercise (ID), sets ODER total_reps, <Satz-Werte>, rest_s?, rest_after_s?
  circuit:  rounds ODER time_cap_s, exercises: [{exercise, <Satz-Werte>}],
            rest_after_exercise_s?, rest_after_round_s?, rest_after_s?, tempo?
  interval: rounds, work_s, rest_s, exercises: [<ID>, ...], rest_after_s?   (HIIT, keine reps)

Satz-Werte:
  reps: Zahl (8) ODER Bereich {min: 8, max: 12} ODER max
  duration_s: Sekunden (30) ODER Bereich {min: 30, max: 45} ODER max   – statt reps, nie beides
  weight_kg: Zahl in kg; weglassen bei Körpergewicht
  per_side: true, wenn „pro Arm/Bein“
  tempo: "3-0-1" (optional)
  progression: (optional, überschreibt defaults)

Pausen in ganzen Sekunden:
  rest_s = zwischen Sätzen (sets), rest_after_exercise_s = zwischen Übungen im Zirkel,
  rest_after_round_s = zwischen Zirkelrunden, rest_after_s = nach dem ganzen Block.

Sonderfälle:
  „X Minuten im Wechsel“      → circuit mit time_cap_s: X*60 statt rounds
  „so viele Sätze bis N Wdh.“ → sets mit total_reps: N statt sets, meist reps: max
  „Gewicht um 5–10 % erhöhen“ o. Ä. → als note am Block; ein wiederholter Durchgang
                                     ist ein eigener, zweiter Block

Progression:
  {type: double, increment_kg: 2.5}   nur mit reps-Bereich
  {type: linear, increment_kg: 2.5}   für feste reps mit Gewicht (z. B. 5x5, 8)
  {type: reps, increment: 1, max_reps: 20}   Körpergewicht: +1 Wdh., sobald alle Sätze geschafft
                                      (max_reps optional)
  {type: none}                        keine Vorschläge

Wichtig:
  - Jede verwendete Übung muss im Katalog "exercises" stehen.
  - Feste reps (z. B. 8) nie mit double-Progression kombinieren; ohne Gewicht type: reps nehmen.
  - Keine weiteren Felder als die oben genannten.
  - Texte (name, note, description) mit Komma oder Doppelpunkt in "Anführungszeichen" setzen.
  - Gängige Übungen bekommen gängige englische IDs (goblet_squat, push_up, pull_up) und
    englische Namen wie in gängigen Übungsdatenbanken – dann werden Bilder automatisch zugeordnet.
    Das Feld image nur setzen, wenn du die ID aus free-exercise-db sicher kennst.
  - Bei ungewöhnlichen oder selbst benannten Übungen muscles angeben (nur Hauptmuskeln, höchstens 3).

Meine Wünsche: <HIER BESCHREIBEN: Ziel, Tage pro Woche, Dauer, vorhandenes Equipment,
Startgewichte, Einschränkungen – oder: „Wandle den angehängten Plan um.“>
````
