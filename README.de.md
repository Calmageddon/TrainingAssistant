# TrainingAssistant

*English version: [README.md](README.md)*

Eine Home-Assistant-Integration (über HACS installierbar) für Krafttraining mit
Fokus auf Hypertrophie und *progressive overload*.

Du arbeitest einen Trainingsplan ab und erfasst jeden Satz, ohne zu tippen: per Knopf und
Sprache. Dein Sprach-Satellit sagt die nächste Übung an und fragt nach jedem Satz
„10 mal 16 Kilo wie geplant?“. Ein Knopfdruck heißt *ja*, sprechen musst du nur, wenn es
anders war („nur acht“). Eine Dashboard-Karte zeigt live, wo du gerade bist. Dort korrigierst
du Sätze per Antippen. Aus dem Verlauf berechnet die Integration Gewicht und
Wiederholungen für das nächste Training.

**Sprachen:** Englisch und Deutsch – Karte, Ansagen, Sprachantworten, Fehlermeldungen,
Anleitung und Vorlagen. Die Sprache folgt deinem Home-Assistant-Profil (sonst Englisch);
die Sprache der Ansagen lässt sich in den Optionen der Integration auch fest einstellen.

## Was drin ist

| Baustein | Inhalt |
|---|---|
| **Ablauf** | Aufwärmen, Sätze (5x5, 3x8–12), Zirkel, HIIT, Cool Down · Zirkel mit Zeitlimit („5 Minuten im Wechsel“) · Sätze bis zu einer Gesamtzahl · `max`-Sätze · pro Seite · Tempo · Pausentimer · Rückgängig, Überspringen, Pause |
| **Sprache** | Ansagen und Rückfragen über einen Assist-Satelliten (`assist_satellite.ask_question`), Zahlen auf Deutsch und Englisch („zwölfeinhalb Kilo“, „acht mal fünfzehn“, "twelve and a half kilos") |
| **Verlauf** | Jeder Satz dauerhaft gespeichert (nicht im HA-Recorder) · Vorschläge per doppelter/linearer/Wiederholungs-Progression · nachträglich korrigierbar |
| **Anstrengung** | „acht, war schwer“ sagen oder *Leicht / Normal / Schwer* antippen: schwer = nächstes Mal nicht steigern, alle leicht = größerer Schritt |
| **Rekorde** | Neue Bestwerte (Gewicht, geschätztes Maximum, Wiederholungen, Zeit) werden angesagt („Neuer Rekord!“), mit 🏆 markiert und als Event gemeldet |
| **Statistik** | Wochenansicht („3 von 4 Trainings diese Woche“ mit Tagen und Muskelgruppen), Wochenziel, Serie, Trainingszeit, Sätze pro Muskelgruppe und Woche, Erholungsstatus je Muskelgruppe |
| **Personen** | Mehrere Personen an einem Tablet: jede mit eigenem Verlauf, eigenen Vorschlägen, Wochenziel und Programm-Position; Pläne sind gemeinsam |
| **Übungsbilder** | Fotos (Start/Ende) aus [free-exercise-db](https://github.com/yuhonas/free-exercise-db) (gemeinfrei), automatisch zugeordnet; beim Plan-Import einmalig geladen, danach lokal |
| **Karte** | `custom:training-assistant-card` mit den Reitern Training, Verlauf und Pläne, wird automatisch geladen |
| **Entitäten** | Tasten *Starten, Weiter, Rückgängig, Pause, Überspringen, Beenden, Abbrechen, Wdh./Gewicht mehr/weniger, Pause länger/kürzer (±15 s)* · Zahlen *Wiederholungen, Gewicht* (z. B. für einen Drehregler) · Auswahl *Person, Programm, Nächstes Workout* · Sensoren *Status, Aktuelle Übung, Fortschritt, Letzter Satz, Trainings diese Woche, Serie* · Kalender *Trainings* |
| **Blueprints** | Zigbee-Knopf · Training per Sprache starten · Signale für HIIT/Pausen (Ton, Licht) |

Die Integration kennt bewusst **keine Hardware**. Ein Knopf „drückt“ die Tasten-Entitäten
(Blueprint), und der Sprach-Satellit wird beim Start mitgegeben. Ohne Geräte läuft das Training
stumm über die Karte.

## Installation

1. HACS → ⋮ → *Benutzerdefinierte Repositories* → `https://github.com/Calmageddon/TrainingAssistant`, Typ *Integration*
2. TrainingAssistant installieren, Home Assistant neu starten
3. Einstellungen → Geräte & Dienste → *Integration hinzufügen* → TrainingAssistant
4. Dashboard bearbeiten → Karte hinzufügen → **TrainingAssistant** (oder `type: custom:training-assistant-card`)

Benötigt Home Assistant 2025.7 oder neuer.

**Optionen** (Integration → *Konfigurieren*): Standard-Satellit, Ansagen an/aus,
Rückfragen an/aus, Wartezeit auf eine Antwort, Sprache der Ansagen (automatisch, Englisch, Deutsch),
Handy-Benachrichtigung (ein `notify`-Dienst wie `mobile_app_…` für Pausenende und neue Rekorde).

## Datenschutz

Beim Import eines Plans lädt Home Assistant die passenden Übungsbilder einmalig von
`raw.githubusercontent.com` und speichert sie unter `<config>/training_assistant/images/`.
Beim Anzeigen der Karte wird nichts aus dem Internet geladen.

## Trainingspläne

**Vorlagen:** 16 bewährte Programme werden mitgeliefert (Kraft & Hypertrophie, Bodyweight ohne
Geräte, Calisthenics von Einstieg bis Fortgeschritten, Kettlebell). Die Vorlagen sind auf Englisch;
übernehmen in der Karte unter *Einstellungen → Vorlagen*, Übersicht und Quellen: [docs/vorlagen.md](docs/vorlagen.md).

Eigene Pläne werden als YAML/JSON in der Karte (*Einstellungen → Eigener Plan*) eingefügt. Die Karte bietet
eine Anleitung und einen Beispielplan zum Herunterladen an. Format, Beispiele und ein fertiger
Prompt für ChatGPT/Claude: [docs/plan-format.de.md](docs/plan-format.de.md).

## Bedienung

| Knopf (Standard im Blueprint) | Wirkung |
|---|---|
| einmal | Satz fertig / weiter · während einer Rückfrage: „wie geplant“ · ohne Training: nächstes Workout starten |
| doppelt | Rückgängig (einen Schritt zurück, dort erfassten Satz verwerfen) |
| lang | Pause / fortsetzen |

Sprachstart: Blueprint *Start a workout by voice* (Training per Sprache starten), z. B. „Hey Jarvis, Training Protocol“.
Rückfragen und Ansagen laufen dann über genau diesen Satelliten.

Satelliten müssen `ask_question` können, also von sich aus ein Gespräch beginnen. Das können z. B.
der Voice PE, ESPHome-Satelliten und *Kiosk Satellite* (auch auf dem Echo Dot 2 mit LineageOS).

### Blueprints importieren

Einstellungen → Automationen & Szenen → Blueprints → *Blueprint importieren*:

- `https://github.com/Calmageddon/TrainingAssistant/blob/main/blueprints/automation/training_assistant/button.yaml`
- `https://github.com/Calmageddon/TrainingAssistant/blob/main/blueprints/automation/training_assistant/voice_start.yaml`
- `https://github.com/Calmageddon/TrainingAssistant/blob/main/blueprints/automation/training_assistant/signals.yaml`

(Bei einem privaten Repo: Datei-Inhalt kopieren und unter `config/blueprints/automation/` ablegen.)

### Aktionen und Events

Aktionen: `training_assistant.start`, `next`, `undo`, `skip`, `pause`, `finish`, `abort`,
`adjust`, `set_value`, `import_plan`, `delete_plan`, `set_program`, `set_next_workout`, `log_set`,
`edit_set`, `get_history`, `get_stats`, `rest_adjust`, `set_profile`. `next`, `log_set` und `edit_set`
nehmen `effort` (`easy`, `normal`, `hard`) an.

**Personen:** Personen legst du unter *Einstellungen → Personen* an. „Wer trainiert?“ erscheint über dem
Startknopf, sobald es mehr als eine Person gibt (auch als Auswahl-Entität *Person* und Aktion
`set_profile`, z. B. für einen NFC-Tag pro Person). Während eines Trainings kann nicht gewechselt werden.
Personen sind keine Home-Assistant-Benutzer, Gäste brauchen also kein Konto. Optional kann ein Admin eine
Person mit einem Home-Assistant-Benutzer verknüpfen (*Einstellungen → Personen*): Öffnet dieser Benutzer die Karte,
z. B. auf seinem Handy, wird seine Person automatisch ausgewählt (einmal beim Öffnen, nie während eines Trainings).

**Programme:** Du bewegst dich in einem *aktiven Programm*. Nach jedem beendeten Training ist das
nächste Workout dieses Programms vorgemerkt, nach dem letzten wieder das erste. Jedes Programm merkt
sich seine Position: Wechselst du kurz in ein anderes (Auswahl „Programm“) und zurück, geht es dort
weiter, wo du warst. Ein einzelnes Workout aus einem anderen Programm startest du über
*Einstellungen → Meine Pläne → Starten*, ohne das aktive Programm zu wechseln.

Event `training_assistant_event` mit `type`: `session_started`, `step`, `set_logged`,
`set_answered`, `rest_over`, `time_cap_over`, `interval_work`, `interval_rest`,
`interval_done`, `paused`, `resumed`, `undo`, `record`, `session_finished`.

## Weitere Sprache hinzufügen

- Karte: Eintrag in `I18N` oben in `frontend/training-assistant-card.js`
- Ansagen: `phrases.py` · Zahlwörter und Antwortwörter: `spoken.py`
- Oberflächentexte und Fehlermeldungen: `translations/<sprache>.json`
- Prüfmeldungen für Pläne: `EN_MESSAGES` in `plan.py` (Ausgangstext ist Deutsch)

## Entwicklung

```bash
scripts/setup        # einmalig: Python-Umgebung mit Home Assistant (braucht uv)
scripts/develop      # Testinstanz auf http://localhost:8123
.venv/bin/python -m pytest tests            # Logik-Tests
.venv/bin/python tools/e2e_test.py          # Praxistest gegen die laufende Testinstanz
.venv/bin/python tools/validate_plan.py mein-plan.yaml
.venv/bin/python tools/build_guide.py       # Anleitungen neu bauen nach Änderungen an docs/plan-format*.md
```

Die Testinstanz enthält einen Test-Satelliten (`scripts/dev_components/fake_voice`), der
Rückfragen mit vorgegebenen Sätzen beantwortet.
