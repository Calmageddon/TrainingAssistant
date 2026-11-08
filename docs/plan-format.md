# Import format for training plans (version 1)

*Deutsche Fassung: [plan-format.de.md](plan-format.de.md)*

A plan is a YAML or JSON file. The exact definition is in
[`schema/plan.schema.json`](../schema/plan.schema.json). Complete examples:
[`guide/example-plan.yaml`](../custom_components/training_assistant/guide/example-plan.yaml) (all block types),
the [templates](../custom_components/training_assistant/templates/) and
[`tests/fixtures/feature-testplan.yaml`](../tests/fixtures/feature-testplan.yaml) (circuit training with
max sets, "per side" and sets up to a total).

Import it in the dashboard card (tab **Settings** → **Own plan** → paste → *Import*) or
with the action `training_assistant.import_plan`. A plan with the same `name` is replaced,
the history is kept.

## Structure

```
Plan
├── exercises   exercise catalog (ID → name, aliases, equipment)
└── workouts    training sessions (e.g. workout 1–4), suggested in rotation
    └── blocks  sections in a fixed order
```

**Exercise IDs** (`goblet_squat`) matter: the integration uses them to match the history,
even across different plans. So an exercise should have the same ID in every plan.

## Exercise images

The card shows photos (start and end position) for each exercise from
[free-exercise-db](https://github.com/yuhonas/free-exercise-db) (public domain, over 870 exercises).
On import, Home Assistant downloads the images of the exercises in the plan once. After that
they are served locally by Home Assistant.

Matching happens automatically via `name`, `aliases` and the exercise ID. Common English and
German names such as "Deadlift"/"Kreuzheben" are recognized. On import the card shows which
exercises did not get an image. You can assign one yourself:

```yaml
exercises:
  javelin_press:
    name: Javelin Press
    image: Dumbbell_Shoulder_Press   # folder name from free-exercise-db/exercises
  burpee:
    name: Burpees
    image: false                     # deliberately no image
```

You can find the image IDs on the [catalog page](https://yuhonas.github.io/free-exercise-db/)
(open an exercise, the ID is in the address) or in the folder
[exercises](https://github.com/yuhonas/free-exercise-db/tree/main/exercises).

## Muscle groups

Weekly sets per muscle group and the recovery status use the muscles of the catalog image. You can set
them yourself – this always takes precedence, e.g. for exercises without an image:

```yaml
exercises:
  trap_bar_deadlift:
    name: Trap Bar Deadlift
    muscles: [quads, glutes, back]
  burpee:
    name: Burpees
    muscles: []        # whole body – deliberately not assigned to a muscle group
```

Groups: `chest`, `back`, `shoulders`, `biceps`, `triceps`, `core`, `quads`, `hamstrings`, `glutes`, `calves`.
Exercises without an image and without `muscles` are listed in the card under "Without muscle group".

## Block types

| Type       | Purpose                                     | Fields                                                     |
|------------|---------------------------------------------|------------------------------------------------------------|
| `warmup`   | Warm-up, ends with the button               | `name`, `duration_s`, `note`                               |
| `sets`     | Sets of one exercise (5x5, 3x8–12)          | `exercise`, `sets` **or** `total_reps`, set values (see below), `rest_s`, `rest_after_s` |
| `circuit`  | Circuit: every exercise 1 set per round     | `rounds` **or** `time_cap_s`, `exercises[]`, `rest_after_exercise_s`, `rest_after_round_s`, `rest_after_s`, `tempo` |
| `interval` | HIIT, purely timed                          | `rounds`, `work_s`, `rest_s`, `exercises[]` (IDs, in rotation), `rest_after_s` |
| `cooldown` | Cool-down                                   | like `warmup`                                              |

Every block can have `name` and `note`. The note is read out when the block is announced,
e.g. "increase the weight by 5–10 %".

### Open-ended blocks

- **Circuit with time cap** ("alternate the two exercises for 5 minutes"): `time_cap_s: 300`
  instead of `rounds`. Rounds continue until time is up. Then you finish the current
  exercise and the next block starts.
- **Sets up to a total** ("20 pull-ups, as many sets as needed"): `total_reps: 20`
  instead of `sets`, usually with `reps: max`.

### Rest

| Field                   | Meaning                                            |
|-------------------------|----------------------------------------------------|
| `rest_s`                | (sets) rest between sets                           |
| `rest_after_exercise_s` | (circuit) rest between two exercises of a round    |
| `rest_after_round_s`    | (circuit) rest between rounds                      |
| `rest_after_s`          | rest after the whole block ("2 minutes break")     |
| `defaults.rest_s`       | default wherever nothing else is set               |

## Set values (in `sets` and for each exercise in a `circuit`)

| Field         | Values                                                        |
|---------------|---------------------------------------------------------------|
| `reps`        | `8` · `{min: 8, max: 12}` · `max` (as many as possible)       |
| `duration_s`  | `30` · `{min: 30, max: 45}` · `max` (hold as long as possible) |
| `weight_kg`   | number; omit = bodyweight                                     |
| `per_side`    | `true` = reps per arm/leg                                     |
| `tempo`       | e.g. `"3-0-1"`, gets announced                                |
| `progression` | see below                                                     |
| `note`        | hint, e.g. "within 45 seconds"                                |

`reps` and `duration_s` are mutually exclusive: exactly one of them.

## Progression (suggestions for the next session)

| `type`   | Rule                                                                  |
|----------|-----------------------------------------------------------------------|
| `double` | +1 rep on the weakest set per session. All sets at the top of the range → `+increment_kg`, back to the bottom of the range. Needs `reps: {min, max}`. |
| `linear` | All sets done with the target reps → `+increment_kg` (e.g. 5x5).      |
| `reps`   | For bodyweight: all sets done with the target → next time `+increment` reps (default 1), up to `max_reps`. After that a hint to use a harder variation. Without `max_reps` the top of a range applies; with a fixed number there is no limit. |
| `none`   | No suggestions, fixed values from the plan.                           |

`defaults.progression` applies to all exercises; individual exercises can override it.
Timed sets and `reps: max` automatically run without progression. Fixed `reps` (e.g. `8`)
don't work with `double`. Use `linear` (with weight), `reps` (bodyweight)
or `none` there.

The suggestions become the target values when a workout starts. So the satellite asks
"10 reps with 18 kilos as planned?" if everything went well last time.

## Validate a plan

```bash
python tools/validate_plan.py my-plan.yaml
```

The integration validates the same way on import and reports errors with a path, e.g.
`workouts/0/blocks/2/exercises/1: exercise 'bench' is not in the 'exercises' catalog`.

---

## Prompt for an LLM

Give the following text together with your wishes to ChatGPT, Claude or similar.
Ideally attach `schema/plan.schema.json` as a file. You can also attach a table,
a photo or a PDF of an existing training plan and ask for it to be converted.

````text
Create a training plan for me in the YAML format "TrainingAssistant version 1".
Follow these rules exactly and output ONLY the YAML code, without explanations.

Top level:
  schema_version: 1          (always exactly 1)
  name: <text>
  description: <text>        (optional)
  goal: hypertrophy | strength | endurance | general   (optional)
  defaults:                  (optional)
    rest_s: <seconds>
    progression: <progression>
  exercises:                 catalog, key = ID in snake_case (a–z, 0–9, _)
    <id>:
      name: <display name>
      aliases: [<other names>]         (optional)
      equipment: bodyweight | dumbbell | kettlebell | barbell | band | machine | cable | other
      note: <technique hint>           (optional)
      image: <image ID from free-exercise-db> (optional, otherwise automatic; false = no image)
      muscles: [chest | back | shoulders | biceps | triceps | core | quads | hamstrings | glutes | calves]
                                       (optional, main muscles; [] = whole body/none)
  workouts:                  list
    - id: <snake_case>
      name: <text>
      blocks: [<block>, ...]

Block types (field "type"), all with optional name and note:
  warmup / cooldown: duration_s?
  sets:     exercise (ID), sets OR total_reps, <set values>, rest_s?, rest_after_s?
  circuit:  rounds OR time_cap_s, exercises: [{exercise, <set values>}],
            rest_after_exercise_s?, rest_after_round_s?, rest_after_s?, tempo?
  interval: rounds, work_s, rest_s, exercises: [<ID>, ...], rest_after_s?   (HIIT, no reps)

Set values:
  reps: number (8) OR range {min: 8, max: 12} OR max
  duration_s: seconds (30) OR range {min: 30, max: 45} OR max   – instead of reps, never both
  weight_kg: number in kg; omit for bodyweight
  per_side: true if "per arm/leg"
  tempo: "3-0-1" (optional)
  progression: (optional, overrides defaults)

Rest in whole seconds:
  rest_s = between sets (sets), rest_after_exercise_s = between exercises in a circuit,
  rest_after_round_s = between circuit rounds, rest_after_s = after the whole block.

Special cases:
  "alternate for X minutes"         → circuit with time_cap_s: X*60 instead of rounds
  "as many sets as needed for N reps" → sets with total_reps: N instead of sets, usually reps: max
  "increase the weight by 5–10 %" or similar → as a note on the block; a repeated pass
                                     is a separate, second block

Progression:
  {type: double, increment_kg: 2.5}   only with a reps range
  {type: linear, increment_kg: 2.5}   for fixed reps with weight (e.g. 5x5, 8)
  {type: reps, increment: 1, max_reps: 20}   bodyweight: +1 rep as soon as all sets are done
                                      (max_reps optional)
  {type: none}                        no suggestions

Important:
  - Every exercise used must be listed in the "exercises" catalog.
  - Never combine fixed reps (e.g. 8) with double progression; without weight use type: reps.
  - No fields other than the ones listed above.
  - Put texts (name, note, description) containing a comma or colon in "quotes".
  - Common exercises get common English IDs (goblet_squat, push_up, pull_up) and
    English names as in common exercise databases – then images are matched automatically.
    Only set the image field if you know the ID from free-exercise-db for sure.
  - For unusual or self-named exercises set muscles (main muscles only, at most 3).
  - Write names and notes in the language I use below.

My wishes: <DESCRIBE HERE: goal, days per week, duration, available equipment,
starting weights, limitations – or: "Convert the attached plan.">
````
