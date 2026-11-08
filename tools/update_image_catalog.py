"""Erzeugt den Katalog-Index für Übungsbilder aus free-exercise-db.

Quelle: https://github.com/yuhonas/free-exercise-db (Unlicense / gemeinfrei)
Aufruf:  .venv/bin/python tools/update_image_catalog.py [lokale exercises.json]

Ohne Argument wird dist/exercises.json von GitHub geladen. Ergebnis:
custom_components/training_assistant/catalog/free_exercise_db.json mit id, name, equipment,
images, muscles (Hauptmuskeln: Wochenvolumen und Erholung) und secondary (Nebenmuskeln: nur Erholung).
Die Bilder selbst lädt die Integration erst beim Import eines Plans.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import urllib.request

SOURCE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
TARGET = Path(__file__).resolve().parent.parent / "custom_components" / "training_assistant" / "catalog" / "free_exercise_db.json"


def main(argv: list[str]) -> int:
    if argv:
        data = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    else:
        with urllib.request.urlopen(SOURCE, timeout=30) as resp:  # noqa: S310 – feste Quelle
            data = json.loads(resp.read())
    entries = sorted(
        ({"id": e["id"], "name": e["name"], "equipment": e.get("equipment"), "images": len(e.get("images", [])),
          "muscles": e.get("primaryMuscles", []), "secondary": e.get("secondaryMuscles", [])}
         for e in data if e.get("images")),
        key=lambda e: e["name"].lower(),
    )
    TARGET.write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{len(entries)} Übungen → {TARGET.relative_to(Path.cwd()) if TARGET.is_relative_to(Path.cwd()) else TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
