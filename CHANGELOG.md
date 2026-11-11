# Changelog

All notable changes to TrainingAssistant. Versions follow [Semantic Versioning](https://semver.org):
patch = fixes, minor = new features, major = stable milestone.
Deutsche Fassung jeweils darunter.

## 0.7.1 – 2026-11-11

- Fix: exercise pictures are always shown in full (head, feet and equipment are no longer cut off), in the current
  exercise, "Up next" and the lists.
  *Deutsch:* Korrektur: Übungsbilder werden immer vollständig gezeigt (Kopf, Füße und Geräte werden nicht mehr
  abgeschnitten) – bei der aktuellen Übung, bei „Als Nächstes“ und in den Listen.

## 0.7.0 – 2026-11-10

- New exercise pictures: a uniform pictogram for every template exercise, including yoga, balance and running, which
  had no picture before. Each person chooses a male or female figure (Plans → People). Exercises in your own plans get a
  picture when their name matches one.
  *Deutsch:* Neue Übungsbilder: ein einheitliches Piktogramm zu jeder Vorlagen-Übung, auch zu Yoga, Gleichgewicht und
  Laufen, die bisher kein Bild hatten. Jede Person wählt eine männliche oder weibliche Figur (Pläne → Personen). Übungen aus eigenen
  Plänen bekommen ein Bild, wenn ihr Name passt.
- The pictures ship with the integration: nothing is downloaded on plan import anymore.
  *Deutsch:* Die Bilder werden mit der Integration ausgeliefert: Beim Plan-Import wird nichts mehr heruntergeladen.

## 0.6.0 – 2026-11-08

- Six new templates: Full Body 3 Days (Gym), Minimal Strength 2 Days, Exercise Snacks, Balance & Leg Strength
  (inspired by the Otago programme), Core Stability Trio (inspired by McGill's "Big 3") and Run Starter 9 Weeks
  (inspired by NHS Couch to 5K, 27 runs in order) in the new group "Endurance".
  *Deutsch:* Sechs neue Vorlagen: Ganzkörper 3 Tage (Studio), Minimal-Kraft 2 Tage, Bewegungs-Snacks, Gleichgewicht &
  Beinkraft (angelehnt an das Otago-Programm), Rumpf-Trio (angelehnt an McGills „Big 3“) und Laufeinstieg in 9 Wochen
  (angelehnt an NHS „Couch to 5K“, 27 Läufe der Reihe nach) in der neuen Gruppe „Ausdauer“.

## 0.5.4 – 2026-11-08

- Phone: the exercise tile grows with its content instead of cutting off the name, target or note; reps and target in one
  line ("Reps · goal 15–30"); the exercise note shows one line and expands on tap.
  *Deutsch:* Handy: Die Übungskarte wächst mit statt Name, Ziel oder Hinweis abzuschneiden; „Wdh. · Ziel 15–30“ in einer
  Zeile; der Hinweis ist einzeilig und klappt beim Antippen auf.
- Block and position (e.g. "Circuit · Strength circuit A · Round 1/3") moved from the exercise tile to a small line under
  the progress bar; the tile only shows the exercise.
  *Deutsch:* Block und Position („Zirkel · Kraftzirkel A · Runde 1/3“) stehen jetzt klein unter dem Fortschrittsbalken statt
  in der Übungskarte.
- Phone: smaller exercise name in the exercise tile.
  *Deutsch:* Handy: kleinerer Übungsname in der Übungskarte.

## 0.5.3 – 2026-11-08

- The workout clock stops while the workout is paused; pauses no longer count towards the workout duration,
  the "last time" comparison or the weekly time in the statistics.
  *Deutsch:* Die Trainingsuhr steht während der Pause still; Pausen zählen nicht mehr zur Trainingsdauer, zum
  Vergleich „letztes Mal“ und zur Wochenzeit in der Statistik.

## 0.5.2 – 2026-11-08

- Start page reordered: week overview first, then program and workout, then *Start workout* (choose, then start).
  On phones the week card and the hint are more compact so the start button stays visible without scrolling.
  *Deutsch:* Startseite neu geordnet – erst die Woche, dann Programm/Workout, dann „Training starten“; auf dem Handy
  kompakter, damit der Start-Knopf ohne Scrollen sichtbar bleibt.
- Week card header: ring, "This week" with status and streak on separate lines, goal stepper on the right
  ("workouts per week").
  *Deutsch:* Kopf der Wochen-Karte – Ring, „Diese Woche“ mit Stand und Serie, rechts der Regler „Workouts pro Woche“.
- Week card: "This week" as a small label top left, ring and streak ("Streak" / "1 week") next to each other,
  "workouts per week" above the goal stepper in the top right; "to go" and "goal reached" removed (the ring shows it).
  *Deutsch:* Wochen-Karte: „Diese Woche“ klein oben links, Ring und Streak nebeneinander, „Workouts pro Woche“ über dem
  Regler oben rechts; „noch 2“ und „Ziel erreicht“ entfallen (zeigt der Ring).

## 0.5.1 – 2026-11-08

- Phone: workout header shows the workout name with the program below and the clock with "last time" on the right;
  the comparison bar is replaced by "last time" turning yellow once you take longer.
  *Deutsch:* Kopfzeile auf dem Handy aufgeräumt – „letztes Mal“ wird gelb statt eines zweiten Balkens.
- Program and workout selection uses a smaller font so long names fit.
  *Deutsch:* Programm- und Workout-Auswahl mit kleinerer Schrift, damit lange Namen passen.
- Week card reorganised: ring with "This week", status and a goal stepper (− 3 +) on top, daily bars below
  (side by side on wide screens).
  *Deutsch:* Wochen-Karte aufgeräumt – Ring, Stand und Ziel-Regler oben, Balken darunter.

## 0.5.0 – 2026-11-08

### New
- **"How did it feel?" after each set:** right after *Set done* a small dialog names the set you just did
  (exercise, set, values) and offers Easy · Normal · Hard. It disappears after 5 seconds (a shrinking line shows
  the time). No answer = normal; you can still change it in the logged sets or the history.
- **HIIT, Tabata and flows use the status bar** like sets: green *Go! · Round 1/8* with countdown during work,
  yellow *Rest* / *Switch* during breaks. The exercise tile only shows the exercise.

### Improved
- **Phone layout during a workout:** plus/minus for reps and weight side by side, compact header and tiles –
  the big button is visible without scrolling (tested at 375 × 667).
- **Settings tabs** fit narrow screens (icon above the label).
- **Exercise history on phones:** one card per exercise instead of a four-column table.
- **Editing a set:** its own panel with larger fields, labelled "How did it feel?", a big Save button.

### Fixed
- Confirming *Discard* / *Finish* no longer scrolls the page to the top on phones.
- The countdown of a running interval is no longer cut off on small screens.

### Deutsch
- **Neu:** „Wie war's?“ als 5-Sekunden-Dialog nach „Satz fertig“ (nennt den Satz, schrumpfende Linie, später
  änderbar). HIIT, Tabata und Flows zeigen Arbeit/Pause in der Statusleiste wie bei Sätzen.
- **Verbessert:** Training passt auf kleine Handys ohne Scrollen, Einstellungs-Reiter auf schmalen Bildschirmen,
  Übungsverlauf als Karten, Satz bearbeiten mit mehr Abstand.
- **Behoben:** „Verwerfen“/„Beenden“ springt auf dem Handy nicht mehr nach oben; Intervall-Countdown wird nicht
  mehr abgeschnitten.

## 0.4.1 and earlier

See the commit history.
