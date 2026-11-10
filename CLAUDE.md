# CLAUDE.md

Hinweise für Claude Code in diesem Repository.

## Projekt

TrainingAssistant: eine Custom Integration für Home Assistant, über HACS installierbar.
Domain `training_assistant`. Sie führt durch einen Trainingsplan (Zirkel, Sätze/5x5,
HIIT), erfasst Reps/Gewicht pro Satz per Knopf und Sprache (`assist_satellite.ask_question`),
speichert den Verlauf dauerhaft und schlägt Gewichte für das nächste Training vor.
**Sprachen: Englisch zuerst, Deutsch als zweite Sprache.** Code-Kommentare sind Deutsch.
Nutzer-sichtbare Texte gibt es auf Englisch und Deutsch:
- UI und Fehlermeldungen: `strings.json`, `translations/en.json`, `translations/de.json`
  (Fehler über `errors.py` → `error("key", …)`, Schlüssel unter `exceptions`).
- Karte: Tabelle `I18N` oben in `frontend/training-assistant-card.js` (Sprache aus `hass.locale`, Rückfall Englisch).
- Ansagen: `phrases.py` (`Speech`), Sprache pro Session in `state["lang"]` (alte Sessions: "de").
  Zahl-/Antworterkennung: `spoken.py` (`LANGS`). Option `voice_language` (auto/en/de).
- Plan-Prüfmeldungen: deutscher Ausgangstext in `plan.py`, englisch über `EN_MESSAGES`
  (`tests/test_plan.py` prüft, dass jede Meldung ein Muster hat). Vorschläge: `reason_key`/`reason_params`
  aus `progression.py`, die Karte übersetzt sie (`sug.<key>`).
- Doku: `README.md`/`docs/plan-format.md`/`docs/templates.md` (Englisch) und
  `README.de.md`/`docs/plan-format.de.md`/`docs/vorlagen.md` (Deutsch) – beide pflegen.
- Vorlagen sind auf Englisch (deutsche Übungsnamen als `aliases`). Die eigenen Pläne des Nutzers in
  `examples/` bleiben Deutsch.

## Architektur-Entscheidungen

- **Keine Hardware in der Integration.** Der Config-Flow fragt keine Geräte ab. Knöpfe
  docken über Blueprints/Automationen an eigene `button`-Entitäten an (Weiter, Rückgängig,
  Pause). Der Satellit wird beim Start der Session als Parameter übergeben. Optional gibt es
  später einen Standard-Satelliten in den Optionen. Ohne Satellit läuft alles stumm über die Karte.
- **Logik gehört in die Integration**, nicht in Automationen: Ablauf-Zustand, Rückfragen
  („8 mal 15 Kilo wie geplant?“), Zahlenerkennung („zwölfeinhalb Kilo“), Progression.
- **Planwerte als Standard:** Knopf = wie geplant. Sprechen muss man nur bei Abweichungen.
  Nicht Verstandenes wird als „unbestätigt“ mit Planwerten gespeichert, und das Training läuft weiter.
- **Speicher:** `homeassistant.helpers.storage.Store`, nicht der HA-Recorder (der löscht
  nach 10 Tagen und fasst zusammen). Jeder Satz muss über Monate erhalten bleiben.
- **Programm-Rotation:** `data["program"]` = aktiver Plan, `data["rotation"][plan_id]` = fälliges Workout je Plan,
  `data["next"]` wird daraus abgeleitet (`_sync_next`). Beenden rückt nur die Position des trainierten Plans weiter,
  das aktive Programm wechselt nur per `set_program`/`set_next`.
- **Progression** regelbasiert (`double`, `linear`, `reps` für Körpergewicht, `none`), ohne LLM.
  `reps` baut auf dem im Satz gespeicherten `target_reps` der letzten Session auf, nicht auf dem Planwert.
- **Personen (Profile):** `data["profiles"]`, aktive Person `data["profile"]`. Die Daten der aktiven Person
  (`PROFILE_KEYS`: sessions, program, rotation, next, active, last_session_id) liegen direkt in `self.data`,
  die der anderen in `data["profile_data"][id]` – beim Wechsel wird getauscht, der übrige Code bleibt unverändert.
  Wechsel nur ohne laufendes Training. Pläne sind gemeinsam. Alte Daten → Profil `p1` (Name des HA-Besitzers).
  Personen sind keine HA-Benutzer; optional `user_id` (Admin verknüpft, ws `link_profile`). Die Karte wählt die
  Person des angemeldeten Benutzers einmal beim Öffnen aus (`_autoSelectProfile`), nie während eines Trainings.
- **Anstrengung** `effort` im Satz ("easy"/"hard", normal = None): per Sprache (`spoken.py`), Karte oder `effort`-Feld.
  Progression: schwer → `hard_hold`, alle leicht → doppelter Schritt (`easy_*`).
- **Rekorde/Statistik** in `stats.py` (ohne HA). Muskelgruppen kommen aus dem Katalog (`muscles` in
  `catalog/exercises.json`, über die Katalog-Zuordnung der Übung; `MUSCLE_GROUPS`). Nebenmuskeln (`secondary`)
  zählen nur für die Erholung, nicht für das Wochenvolumen. `muscles` im Plan hat Vorrang (dann ohne Nebenmuskeln). Rekord wird nach
  `set_logged`/`set_answered` geprüft (`_check_record`), steht als `record` im Satz, Event `record`.
- **Flow** (`flow`): zeitgesteuerte Abfolge mit eigener Dauer je Übung (Yoga, 30-20-10). `build_steps` macht daraus
  einen `interval`-Schritt mit `segments` (auch klassische HIIT-Blöcke haben `segments`). Der Manager-Runner
  speichert jeden fertigen Abschnitt als Satz (`Engine.log_segment`). Icon: `brand/icon.png` (Quelle `assets/icon.svg`).
- **Übungsbilder** (Piktogramme) aus dem privaten Repo `uebungs-piktogramme` (`zuordnung.json`), übernommen mit
  `python3 tools/import_pictos.py ../uebungs-piktogramme` nach `pictos/<m|w>/<Bild>/<n>.jpg` (512 px, mitgeliefert,
  URL `/training_assistant/pictos/<VERSION>/…`) und `catalog/pictos.json`. Dort nur Kennungen/Namen aus den Vorlagen
  (private Pläne nicht!). Zuordnung `Pictos.match`: Kennung → `image: false` → Name/Aliase = Vorlagen- oder Bildname →
  `image`/Katalog-ID. Im Plan: `images` = Katalog-ID (Muskelgruppen), `pictos` = Bild (bei jedem Start neu berechnet).
  Figur `m`/`w` pro Person (`profile.figure`, ws `profile` action `figure`); `single_images` = ohne Endbild.
- **HIIT** (`interval`) ist zeitgesteuert: Signaltöne/Licht statt Sprache, weil TTS zu langsam ist.

## Code-Aufbau (custom_components/training_assistant/)

- `plan.py` – Prüfung beim Import und Zerlegung eines Workouts in Schritte (`build_steps`). Ohne HA-Abhängigkeit.
- `engine.py` – Ablauf als reine Zustandsmaschine: ändert das Session-dict und liefert „Effekte“
  (announce, ask, rest, block_timer, interval_start, event, finished …). Ohne HA-Abhängigkeit.
- `progression.py`, `spoken.py` – Vorschläge und Zahlenerkennung. Ohne HA-Abhängigkeit.
- `stats.py` – Rekorde, Woche, Serie, Zeit, Muskelvolumen, Erholung. Ohne HA-Abhängigkeit.
- `manager.py` – führt Effekte in HA aus (Store, Satellit, Timer, Events), Verlauf, Pläne.
- `services.py`, `websocket.py` – Aktionen bzw. Befehle für die Karte. `button/calendar/number/select/sensor.py` – Entitäten.
- `frontend/training-assistant-card.js` – Karte ohne Build-Schritt. Wird per `add_extra_js_url` geladen,
  in der URL steckt eine Prüfsumme gegen den Browser-Cache.

## Importformat

- Schema: `schema/plan.schema.json` (JSON Schema 2020-12), Doku und LLM-Prompt in `docs/plan-format.md` (en)
  und `docs/plan-format.de.md` (de),
  Beispiel in `examples/ganzkoerper.yaml`, neutraler Testplan in `tests/fixtures/feature-testplan.yaml`.
- **Private Pläne** des Nutzers (nach einem Buch) liegen nur lokal in `private/plans/` (gitignored).
  Das Repo ist öffentlich: diese Pläne, ihre Namen und Übungsnamen daraus nie committen oder in Doku/Tests verwenden.
- Schema-Änderungen an diesen Stellen nachziehen: `schema/plan.schema.json`, `docs/plan-format.md` und
  `docs/plan-format.de.md` (inkl. Prompt), `validate_plan()` in `plan.py` (+ `EN_MESSAGES`), Anleitungstexte in
  `tools/build_guide.py`. Danach `tools/validate_plan.py examples/*.yaml`, `tools/build_guide.py`
  (Anleitungen `guide/guide-custom-plans.txt` + `guide/example-plan.yaml` bzw. `guide/anleitung-eigene-plaene.txt`
  + `guide/beispiel-plan.yaml`) und die Tests – `tests/test_guide.py` schlägt fehl, wenn eine Anleitung veraltet ist.
  Neue optionale Felder sind kompatibel, inkompatible Änderung → `schema_version` erhöhen.

## Vorlagen

- `custom_components/training_assistant/templates/*.yaml` werden mit ausgeliefert und in der Karte
  unter Einstellungen → Vorlagen angeboten (nicht automatisch importiert). Dateiname beginnt mit Gruppe und Reihenfolge (z. B. `kraft-1-…`)
  (`kraft-`, `bodyweight-`, `calisthenics-`, `kettlebell-`, `hiit-`, `yoga-`; Symbol in `TEMPLATE_GROUPS`, Titel übersetzt die Karte über `tg.<gruppe>`).
  Übersicht und Quellen: `docs/templates.md` / `docs/vorlagen.md`.
- Eigene Namen, „angelehnt an“ bekannte Programme – keine Markennamen als Planname, keine kopierten Texte.
- In YAML-Flow-Schreibweise `{ … }` Hinweise mit Komma in Anführungszeichen setzen (sonst Prüffehler).
- `tests/test_templates.py` prüft Gültigkeit, Zerlegung und Bild-IDs.

## Entwicklung

- Lokale Testinstanz: `scripts/setup` (einmalig), dann `scripts/develop` → http://localhost:8123.
  Die Konfiguration liegt in `config/`, nur `configuration.yaml` wird eingecheckt.
  Python 3.14 über `uv`, getestet mit HA 2026.11.0.
- In `config/configuration.yaml` **kein `default_config:`**: Es enthält Bluetooth, und macOS
  beendet den Prozess dann hart (Exit 137). Benötigte Integrationen einzeln eintragen.
- Login der Testinstanz: `config/dev-login.txt` (gitignored, nur lokal). Test-Dashboard: `/training-test/live`.
- Tests: `.venv/bin/python -m pytest tests` (reine Logik) und `.venv/bin/python tools/e2e_test.py` (bricht ab, wenn in der Testinstanz ein Training läuft – nie mit `--force`, solange der Nutzer dort trainiert)
  (gegen die laufende Testinstanz, inkl. Sprach-Rückfragen über den Test-Satelliten
  `scripts/dev_components/fake_voice`, der `assist_satellite.announce/ask_question` ersetzt).
- **Das echte Home Assistant des Nutzers ist ein Live-System.** Installieren, Neustarten oder
  Ändern dort nur nach gezeigtem Plan und ausdrücklicher Freigabe. Lesen ist erlaubt.
  `tools/e2e_test.py` niemals gegen das echte HA ausführen.
- Mindestversion HA: 2025.7 (`hacs.json`), wegen `assist_satellite.ask_question`.
- Geplante Hardware des Nutzers: Echo Dot 2 mit Kiosk Satellite (LineageOS) oder TECHO5, dazu ein Zigbee-Knopf.
  Ob `ask_question` auf dem echten Gerät funktioniert, ist noch nicht getestet.
- GitHub: öffentliches Repo `Calmageddon/TrainingAssistant` (Installation per HACS). Keine Zugangsdaten committen.

## Versionen und Releases

- Versionen nach Major.Minor.Patch (Patch = Korrektur, Minor = neue Funktion, Major = stabil). Steht in `const.py`,
  `manifest.json` und `CARD_VERSION` der Karte – alle drei gleich halten.
- Jede ausgelieferte Version: Eintrag in `CHANGELOG.md` (en + de), Commit, Tag `vX.Y.Z` und GitHub-Release mit den
  Notizen (`gh release create`). Ohne Release zeigt HACS nur ein Commit-Kürzel. Kleine Änderungen sammeln.
- Das Repo ist öffentlich: Release erst nach ausdrücklicher Freigabe.
- Keine „Co-Authored-By: Claude“-Zeilen in Commits oder PRs.

