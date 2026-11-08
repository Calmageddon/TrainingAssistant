"""Prüft Trainingsplan-Dateien (YAML oder JSON) gegen das Importformat.

Aufruf:  python tools/validate_plan.py examples/ganzkoerper.yaml [weitere Dateien …]

Zwei Stufen:
1. Struktur: JSON-Schema in schema/plan.schema.json (falls „jsonschema“ installiert ist)
2. Inhalt: dieselbe Prüfung, die die Integration beim Import macht
   (custom_components/training_assistant/plan.py), z. B. ob jede Übung im Katalog steht.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "plan.schema.json"
PLAN_PY = ROOT / "custom_components" / "training_assistant" / "plan.py"


def _load_plan_module():
    spec = importlib.util.spec_from_file_location("ta_plan", PLAN_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    plan_mod = _load_plan_module()
    try:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    except ImportError:
        validator = None
        print("Hinweis: „jsonschema“ nicht installiert – nur Inhaltsprüfung.")

    failed = False
    for name in argv:
        text = Path(name).read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as err:
            errors = [f"Datei lässt sich nicht lesen: {err}"]
        else:
            errors = []
            if validator:
                errors = [
                    f"Schema {'/'.join(map(str, e.absolute_path)) or '(oben)'}: {e.message}"
                    for e in validator.iter_errors(data)
                ]
            errors += plan_mod.validate_plan(data)
        if errors:
            failed = True
            print(f"✗ {name}")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"✓ {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
