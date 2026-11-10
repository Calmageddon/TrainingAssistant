"""Konstanten für TrainingAssistant."""

DOMAIN = "training_assistant"
VERSION = "0.7.0"

# Version des Importformats für Trainingspläne (siehe schema/plan.schema.json)
PLAN_SCHEMA_VERSION = 1

STORAGE_KEY = DOMAIN
STORAGE_VERSION = 1

# Dispatcher-Signal: Zustand hat sich geändert (Entitäten + Karte aktualisieren)
SIGNAL_UPDATE = f"{DOMAIN}_update"
# HA-Event für Automationen (Signaltöne, Licht …)
EVENT_NAME = f"{DOMAIN}_event"

# Optionen
CONF_DEFAULT_SATELLITE = "default_satellite"
CONF_ASK_AFTER_SET = "ask_after_set"
CONF_ANNOUNCE = "announce"
CONF_QUESTION_TIMEOUT = "question_timeout"
CONF_VOICE_LANGUAGE = "voice_language"
CONF_NOTIFY = "notify_service"  # z. B. "mobile_app_pixel" – Handy-Hinweis bei Pausenende und Rekord

DEFAULT_QUESTION_TIMEOUT = 20
DEFAULT_WEEKLY_GOAL = 3
REST_STEP_S = 15  # Pausentimer ±15 s

# Dashboard-Karte
CARD_FILENAME = "training-assistant-card.js"
CARD_URL = f"/{DOMAIN}/{CARD_FILENAME}"

# Satz-Status
SET_PLANNED = "planned"  # Planwerte übernommen (Knopf, ohne Rückfrage)
SET_PENDING = "pending"  # Rückfrage läuft
SET_CONFIRMED = "confirmed"  # per Sprache/Knopf bestätigt
SET_CORRECTED = "corrected"  # per Sprache korrigiert
SET_UNCONFIRMED = "unconfirmed"  # Rückfrage ohne verwertbare Antwort
SET_EDITED = "edited"  # nachträglich an der Karte geändert
SET_SKIPPED = "skipped"

# Phasen einer Session
PHASE_READY = "ready"  # Block angesagt, wartet auf Knopf
PHASE_ACTIVE = "active"  # Übung/Satz läuft
PHASE_INTERVAL = "interval"  # HIIT läuft zeitgesteuert
PHASE_FINISHED = "finished"

# Übungsbilder (Piktogramme): mitgeliefert unter pictos/<m|w>/<Bild>/<n>.jpg.
# Die Version steht in der Adresse, damit der Browser nach einem Update neue Bilder lädt.
IMAGES_URL = f"/{DOMAIN}/pictos/{VERSION}"

# So viele vergangene Trainings zeigen die Verlaufsdiagramme (ca. 4 Wochen)
CHART_POINTS = 8

# Anleitung und Beispielplan (Download in der Karte)
GUIDE_URL = f"/{DOMAIN}/guide"
