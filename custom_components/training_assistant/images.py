"""Übungen dem Übungskatalog und den Übungsbildern (Piktogrammen) zuordnen.

Ohne Home-Assistant-Abhängigkeiten.

Katalog (`catalog/exercises.json`): liefert die Muskelgruppen einer Übung. Zuordnung pro Übung im Plan:
1. Feld `image` im Plan: Katalog-ID (z. B. "Goblet_Squat") oder false (= keine)
2. sonst automatisch über Name, Aliase und Übungs-ID:
   a) exakter Treffer nach Vereinheitlichung („Push-Ups“ = „Pushups“, „Chin-ups“ = „Chin-Up“)
   b) handgepflegte Liste gängiger Übungen (COMMON), auch mit deutschen Namen
   c) wie a), aber ohne Equipment-Wörter („Barbell Romanian Deadlift“ = „Romanian Deadlift“)
   Bewusst ohne unscharfe Suche: lieber kein Bild als ein falsches.

Bilder (`catalog/pictos.json`, Dateien unter `pictos/<m|w>/<Bild>/<n>.jpg`, siehe tools/import_pictos.py):
1. Übungs-Kennung aus den mitgelieferten Vorlagen
2. `image: false` = kein Bild
3. Name, Aliase oder Kennung = Name aus den Vorlagen oder Bildname („Bodyweight Hip Thrust“)
4. Feld `image` bzw. die Katalog-ID, wenn es dazu ein Bild gibt
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

CATALOG_FILE = Path(__file__).parent / "catalog" / "exercises.json"
PICTOS_FILE = Path(__file__).parent / "catalog" / "pictos.json"
FIGURES = ("m", "w")
DEFAULT_FIGURE = "m"

EQUIPMENT_WORDS = {
    "barbell", "dumbbell", "kettlebell", "bodyweight", "body", "weight", "bw", "db", "kb", "cable",
    "machine", "band", "smith", "ez", "bar", "weighted",
}

# Gängige Bezeichnungen → Katalog-ID (Schlüssel werden mit norm() vereinheitlicht)
COMMON: dict[str, str] = {
    # Kniebeugen
    "squat": "Barbell_Squat", "back squat": "Barbell_Squat", "kniebeuge": "Barbell_Squat", "kniebeugen": "Barbell_Squat",
    "front squat": "Front_Barbell_Squat", "air squat": "Bodyweight_Squat", "bodyweight squat": "Bodyweight_Squat",
    "jump squat": "Freehand_Jump_Squat", "bulgarian split squat": "Split_Squat_with_Dumbbells",
    "split squat": "Split_Squat_with_Dumbbells",
    # Kreuzheben, Hüfte
    "deadlift": "Barbell_Deadlift", "kreuzheben": "Barbell_Deadlift",
    "romanian deadlift": "Romanian_Deadlift", "rdl": "Romanian_Deadlift", "rumänisches kreuzheben": "Romanian_Deadlift",
    "hip thrust": "Barbell_Hip_Thrust", "glute bridge": "Barbell_Glute_Bridge",
    "single leg hip raise": "Single_Leg_Glute_Bridge", "single leg glute bridge": "Single_Leg_Glute_Bridge",
    "kettlebell swing": "One-Arm_Kettlebell_Swings", "two arm kettlebell swing": "One-Arm_Kettlebell_Swings",
    "reverse lunge": "Dumbbell_Rear_Lunge", "lunge": "Dumbbell_Lunges", "ausfallschritt": "Dumbbell_Lunges",
    # Drücken
    "push up": "Pushups", "liegestütz": "Pushups", "liegestütze": "Pushups",
    "bench press": "Barbell_Bench_Press_-_Medium_Grip", "bankdrücken": "Barbell_Bench_Press_-_Medium_Grip",
    "dumbbell bench press": "Dumbbell_Bench_Press", "incline dumbbell press": "Incline_Dumbbell_Press",
    "incline dumbbell chest press": "Incline_Dumbbell_Press",
    "overhead press": "Barbell_Shoulder_Press", "shoulder press": "Dumbbell_Shoulder_Press",
    "dumbbell overhead press": "Dumbbell_Shoulder_Press", "schulterdrücken": "Dumbbell_Shoulder_Press",
    "lateral raise": "Side_Lateral_Raise", "seitheben": "Side_Lateral_Raise",
    "dumbbell fly": "Dumbbell_Flyes", "rear delt fly": "Reverse_Flyes",
    # Ziehen
    "pull up": "Pullups", "klimmzug": "Pullups", "klimmzüge": "Pullups", "chin up": "Chin-Up",
    "bent over row": "Bent_Over_Barbell_Row", "barbell row": "Bent_Over_Barbell_Row",
    "single arm dumbbell row": "One-Arm_Dumbbell_Row", "one arm dumbbell row": "One-Arm_Dumbbell_Row",
    "dumbbell row": "One-Arm_Dumbbell_Row", "rudern": "Bent_Over_Barbell_Row",
    "cable row": "Seated_Cable_Rows", "upright row": "Upright_Barbell_Row", "face pull": "Face_Pull",
    "shrug": "Barbell_Shrug", "dumbbell shrug": "Dumbbell_Shrug",
    "bicep curl": "Dumbbell_Bicep_Curl", "biceps curl": "Dumbbell_Bicep_Curl", "curl": "Barbell_Curl",
    # Rumpf
    "plank": "Plank", "unterarmstütz": "Plank", "side plank": "Side_Bridge", "seitstütz": "Side_Bridge",
    "hanging knee raise": "Hanging_Leg_Raise", "hanging leg raise": "Hanging_Leg_Raise",
    "leg raise": "Flat_Bench_Lying_Leg_Raise", "beinheben": "Flat_Bench_Lying_Leg_Raise",
    "crunch": "Crunches", "russian twist": "Russian_Twist", "mountain climber": "Mountain_Climbers",
    # Beine (Geräte)
    "calf raise": "Standing_Calf_Raises", "wadenheben": "Standing_Calf_Raises", "seated calf raise": "Seated_Calf_Raise",
    "leg press": "Leg_Press", "beinpresse": "Leg_Press", "leg curl": "Lying_Leg_Curls", "leg extension": "Leg_Extensions",
}


def norm(text: str, *, strip_equipment: bool = False) -> str:
    """Vereinheitlicht einen Übungsnamen für den Vergleich."""
    text = text.lower().replace("-", "").replace("'", "").replace("’", "")
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    words = re.findall(r"[a-z0-9]+", text)
    words = [w[:-1] if len(w) >= 3 and w.endswith("s") and not w.endswith("ss") else w for w in words]
    if strip_equipment:
        words = [w for w in words if w not in EQUIPMENT_WORDS]
    # ohne Leerzeichen: „Single-Arm Row“ = „Single Arm Row“, „Push-Ups“ = „Pushups“
    return "".join(words)


class Catalog:
    def __init__(self, entries: list[dict[str, Any]]) -> None:
        self.by_id = {e["id"]: e for e in entries}
        self._exact: dict[str, str] = {}
        self._stripped: dict[str, str] = {}
        for e in entries:
            self._exact.setdefault(norm(e["name"]), e["id"])
            self._stripped.setdefault(norm(e["name"], strip_equipment=True), e["id"])
        self._common = {norm(k): v for k, v in COMMON.items() if v in self.by_id}

    @classmethod
    def load(cls, path: Path = CATALOG_FILE) -> Catalog:
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def match(self, names: list[str]) -> str | None:
        """Katalog-ID für die erste passende Bezeichnung (Name, dann Aliase)."""
        names = [n for n in names if n]
        for n in names:
            if (cid := self._exact.get(norm(n))) is not None:
                return cid
        for n in names:
            for key in (norm(n), norm(n, strip_equipment=True)):
                if key and (cid := self._common.get(key)) is not None:
                    return cid
        for n in names:
            key = norm(n, strip_equipment=True)
            if key and (cid := self._stripped.get(key)) is not None:
                return cid
        return None

    def image_count(self, cid: str) -> int:
        return int(self.by_id.get(cid, {}).get("images", 0))


def map_plan(plan: dict, catalog: Catalog) -> dict[str, str | None]:
    """Übungs-ID im Plan → Katalog-ID (oder None)."""
    result: dict[str, str | None] = {}
    for ex_id, ex in plan.get("exercises", {}).items():
        explicit = ex.get("image")
        if explicit is False:
            result[ex_id] = None
        elif isinstance(explicit, str):
            result[ex_id] = explicit if explicit in catalog.by_id else None
        else:
            result[ex_id] = catalog.match([ex.get("name", ""), *ex.get("aliases", []), ex_id.replace("_", " ")])
    return result


class Pictos:
    """Übungsbilder: Bildname → Anzahl der Bilder (1 = nur eine Haltung, 2 = Start und Ende)."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.images: dict[str, int] = {k: int(v) for k, v in data.get("images", {}).items()}
        self.by_exercise: dict[str, str] = dict(data.get("exercises", {}))
        self._names: dict[str, str] = {}
        for name, bild in data.get("names", {}).items():
            self._names.setdefault(norm(name), bild)
        for bild in self.images:
            self._names.setdefault(norm(bild.replace("_", " ")), bild)

    @classmethod
    def load(cls, path: Path = PICTOS_FILE) -> Pictos:
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def single(self) -> list[str]:
        """Bilder mit nur einer Haltung (kein Endbild)."""
        return sorted(k for k, v in self.images.items() if v < 2)

    def match(self, ex_id: str, ex: dict, catalog_id: str | None) -> str | None:
        if ex_id in self.by_exercise:
            return self.by_exercise[ex_id]
        if ex.get("image") is False:
            return None
        for name in (ex.get("name", ""), *ex.get("aliases", []), ex_id.replace("_", " ")):
            if name and (bild := self._names.get(norm(name))) is not None:
                return bild
        explicit = ex.get("image")
        if isinstance(explicit, str) and explicit in self.images:
            return explicit
        return catalog_id if catalog_id in self.images else None


def map_pictos(plan: dict, pictos: Pictos, catalog_ids: dict[str, str | None]) -> dict[str, str | None]:
    """Übungs-ID im Plan → Bildname (oder None)."""
    return {
        ex_id: pictos.match(ex_id, ex, catalog_ids.get(ex_id))
        for ex_id, ex in plan.get("exercises", {}).items()
    }
