# Changelog

All notable changes to TrainingAssistant. Versions follow [Semantic Versioning](https://semver.org):
patch = fixes, minor = new features, major = stable milestone.
Deutsche Fassung jeweils darunter.

## 0.11.0 – 2026-11-14

- Plan editor in the card (*Settings → Editor*): build your own plans with workouts, blocks and exercises – pick
  exercises with pictures from a list, set reps, weight or time, rests and progression. Templates are edited as a copy.
  Pasting YAML/JSON still works under *Own plan*.
  *Deutsch:* Plan-Editor in der Karte (*Einstellungen → Editor*): eigene Pläne mit Workouts, Blöcken und Übungen
  bauen – Übungen mit Bild aus einer Liste wählen, Wiederholungen, Gewicht oder Zeit, Pausen und Progression einstellen.
  Vorlagen bearbeitet man als Kopie. YAML/JSON einfügen geht weiter unter *Eigener Plan*.
- The card now shares its interface with the Hero Upgrade web app, so both get the same improvements: search in plans
  and templates, plans grouped by category, recovery colours in six steps (red to green, with legend), a clearer
  "How did it feel?" prompt with a close button, and consistent icons.
  *Deutsch:* Die Karte teilt sich jetzt die Oberfläche mit der Web-App Hero Upgrade, beide bekommen dieselben
  Verbesserungen: Suche in Plänen und Vorlagen, Pläne nach Kategorie gruppiert, Erholungsfarben in sechs Stufen (rot bis
  grün, mit Legende), ein deutlicherer „Wie war's?“-Dialog mit Schließen-Knopf und einheitliche Symbole.
- Exercise thumbnails show the end pose; timed one-sided flow segments show the side.
  *Deutsch:* Kleine Übungsbilder zeigen die Endpose; einseitige Flow-Abschnitte zeigen die Seite.

## 0.10.0 – 2026-11-14

- Light signal (optional): an RGB light shows the phase of the workout – green while you train (bright for a moment
  when a rest ends), yellow during rests and side switches, red in the last 3 seconds before you go, gold for a new
  record. Pick the light in the options, pass `light:` when starting, or let TrainingAssistant use the light of the
  satellite's device (e.g. the LED ring of the Voice PE). Paused, waiting or finished, the light returns to how it was.
  *Deutsch:* Lichtsignal (optional): eine RGB-Lampe zeigt die Phase des Trainings – grün beim Trainieren (kurz hell,
  wenn eine Pause endet), gelb in Pausen und beim Seitenwechsel, rot in den letzten 3 Sekunden vor dem Start, golden bei
  einem neuen Rekord. Lampe in den Optionen wählen, beim Start `light:` mitgeben oder das Licht am Gerät des Satelliten
  nutzen lassen (z. B. den LED-Ring des Voice PE). Pausiert, wartend oder nach dem Training ist die Lampe wie vorher.
- Card: tap an exercise picture (workout preview, templates, history) to see it large with start and end pose.
  *Deutsch:* Karte: Tippen auf ein Übungsbild (Workout-Vorschau, Vorlagen, Verlauf) zeigt es groß mit Start- und Endpose.
- One-sided exercises show "/side" right at the big number ("10 /side"); the "Up next" list stays on one line.
  *Deutsch:* Einseitige Übungen zeigen „/Seite“ direkt an der großen Zahl („10 /Seite“); die Liste „Danach“ bleibt einzeilig.
- The "New record" banner no longer takes half of the status line during the next exercise – records stay in the list
  of logged sets and in the summary.
  *Deutsch:* Das Banner „Neuer Rekord“ nimmt während der nächsten Übung nicht mehr die halbe Statuszeile ein – Rekorde
  stehen weiter in der Liste der erfassten Sätze und im Abschluss.
- Muscle groups checked for all template exercises: 23 corrected (e.g. reverse lunge: quads and glutes instead of back),
  wall sit and L-sit now have muscle groups.
  *Deutsch:* Muskelgruppen aller Vorlagen-Übungen geprüft: 23 korrigiert (z. B. Ausfallschritt rückwärts: Oberschenkel
  vorn und Po statt Rücken), Wandsitzen und L-Sit haben jetzt Muskelgruppen.
- Recovery: muscles that only helped (secondary) count with a 24-hour head start – right after training at most
  "recovering", ready after one day. Main muscles count as before.
  *Deutsch:* Erholung: Muskeln, die nur mitgeholfen haben (sekundär), zählen mit 24 Stunden Vorsprung – direkt danach
  höchstens „erholt sich“, nach einem Tag bereit. Hauptmuskeln zählen wie bisher.

## 0.9.0 – 2026-11-13

- One-sided timed exercises (e.g. side plank) run per side: left, 5 s to switch, then right – the time counts for each
  side. With a satellite the switch is announced; the card shows which side is on and a "Switch sides" countdown.
  New optional exercise field `unilateral` in the plan format; 33 template exercises are marked.
  *Deutsch:* Einseitige Zeitübungen (z. B. Seitstütz) laufen pro Seite: links, 5 s Seitenwechsel, dann rechts – die Zeit
  gilt pro Seite. Mit Satellit wird der Wechsel angesagt; die Karte zeigt, welche Seite dran ist, und einen Countdown
  zum Wechsel. Neues optionales Übungsfeld `unilateral` im Planformat; 33 Übungen der Vorlagen sind markiert.
- Summary after the workout: duration, sets, reps, time under tension, weight moved, muscles, new bests, what got better
  than last time, what changes next time, week and streak. Short version when you finish early.
  *Deutsch:* Abschluss nach dem Training: Dauer, Sätze, Wiederholungen, Zeit unter Spannung, bewegtes Gewicht, Muskeln,
  neue Bestwerte, was besser wurde als letztes Mal, was sich beim nächsten Mal ändert, Woche und Serie. Kurze Fassung,
  wenn man vorzeitig beendet.
- Timed sets now progress: all times done → +5 s next time (all easy → +10 s), with no upper limit.
  *Deutsch:* Sätze nach Zeit steigern sich: alle Zeiten geschafft → beim nächsten Mal +5 s (alles leicht → +10 s), ohne
  Obergrenze.
- 7-Minute Circuit: 5 s to switch, so one round takes 7 minutes.
  *Deutsch:* 7-Minuten-Zirkel: 5 s Wechsel, eine Runde dauert damit 7 Minuten.
- The one-arm kettlebell swing is its own exercise with its own picture; earlier swings of that template move along.
  *Deutsch:* Der einarmige Kettlebell Swing ist eine eigene Übung mit eigenem Bild; bisherige Swings dieser Vorlage
  ziehen mit um.

## 0.8.0 – 2026-11-11

- Templates: tap a program to see its workouts and exercises with reps, weight or time before adding it. Several
  workouts can be switched with buttons; nothing is added until you tap "Add".
  *Deutsch:* Vorlagen: Tippen auf ein Programm zeigt seine Workouts und Übungen mit Wiederholungen, Gewicht oder Zeit,
  bevor man es übernimmt. Mehrere Workouts lassen sich per Knopf umschalten; übernommen wird erst mit „Übernehmen“.
- Template categories can be collapsed; all are collapsed when the list opens.
  *Deutsch:* Die Kategorien der Vorlagen lassen sich einklappen; beim Öffnen sind alle zugeklappt.
- HIIT blocks in the workout preview show their exercises with pictures. "1 sets" now reads "1 set".
  *Deutsch:* HIIT-Blöcke in der Workout-Vorschau zeigen ihre Übungen mit Bild. Aus „1 Sätze“ wird „1 Satz“.

## 0.7.3 – 2026-11-11

- Updated exercise pictures: start and end position of each exercise are aligned, so the movement preview runs
  smoothly (equipment and standing foot stay in place). Plank and Feet-Elevated Plank now use a single picture; Push
  Press shows the standing overhead press.
  *Deutsch:* Überarbeitete Übungsbilder: Start- und Endposition jeder Übung sind aufeinander ausgerichtet, die Bewegung
  läuft dadurch ruhig (Gerät und Standfuß bleiben an ihrem Platz). Plank und Feet-Elevated Plank haben nur noch ein
  Bild; Push Press zeigt das Bild der stehenden Schulterpresse.

## 0.7.2 – 2026-11-11

- New pictures for Bulgarian Split Squat (both figures): the end position now shows the deep squat instead of the same
  height.
  *Deutsch:* Neue Bilder für Bulgarian Split Squat (beide Figuren): Das Endbild zeigt jetzt die tiefe Position statt
  derselben Höhe.

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
