"""Übernimmt die Übungsbilder (Piktogramme) aus dem Bilder-Repo in die App.

Aufruf (macOS, nutzt `sips` zum Verkleinern):
    python3 tools/import_pictos.py ../uebungs-piktogramme

Liest `zuordnung.json` des Bilder-Repos und schreibt
- die Bilder verkleinert (512 px) nach custom_components/training_assistant/pictos/<m|w>/<Bild>/<n>.jpg
- die Zuordnung nach custom_components/training_assistant/catalog/pictos.json:
  {"exercises": {Übungs-Kennung: Bild}, "names": {Name: Bild}, "images": {Bild: Anzahl}}

Nur Bilder aus zuordnung.json werden übernommen (beide Figuren abgenommen).
Bilder, die es nicht mehr gibt, werden entfernt.
Kennungen und Namen kommen nur aus den mitgelieferten Vorlagen (--plans) in die Datei: zuordnung.json
enthält auch Übungen aus privaten Plänen, die nicht veröffentlicht werden dürfen. Die Bilder selbst
werden alle übernommen; eigene Pläne finden sie über den Bildnamen (z. B. „Bodyweight Hip Thrust“).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "custom_components" / "training_assistant" / "pictos"
PLANS = ROOT / "custom_components" / "training_assistant" / "templates"
OUT_JSON = ROOT / "custom_components" / "training_assistant" / "catalog" / "pictos.json"
FIGURES = ("m", "w")
SIZE, QUALITY = 512, 80


def plan_keys(plans: Path) -> set[str]:
    """Übungs-Kennungen (Schlüssel unter `exercises:`) aller Vorlagen, ohne YAML-Bibliothek."""
    keys: set[str] = set()
    for file in plans.glob("*.yaml"):
        section = re.search(r"^exercises:\n((?:[ #].*\n|\n)*)", file.read_text(encoding="utf-8"), re.M)
        if section:
            keys.update(re.findall(r"^  ([A-Za-z0-9_]+):", section.group(1), re.M))
    return keys


def plan_names(plans: Path) -> set[str]:
    """Übungsnamen und Aliase aller Vorlagen (name: … und aliases: […]), ohne YAML-Bibliothek."""
    names: set[str] = set()
    for file in plans.glob("*.yaml"):
        text = file.read_text(encoding="utf-8")
        names.update(m.strip() for m in re.findall(r"""\bname:\s*["']?([^"'\n,}]+)""", text))
        for group in re.findall(r"aliases:\s*\[([^\]]*)\]", text):
            names.update(a.strip().strip("\"'") for a in group.split(","))
    return names


def build(source: Path, out_dir: Path, out_json: Path, plans: Path) -> None:
    mapping = json.loads((source / "zuordnung.json").read_text(encoding="utf-8"))["zuordnung"]
    public = plan_keys(plans)
    # Namen nur, wenn sie genau so in einer Vorlage stehen (gemeinsame Kennungen tragen auch private Namen)
    template_names = plan_names(plans)
    exercises = {key: entry["bild"] for key, entry in sorted(mapping.items()) if key in public}
    images: dict[str, int] = {}
    names: dict[str, str] = {}
    for key, entry in mapping.items():
        images[entry["bild"]] = int(entry["bilder"])
        if key in public:
            for name in entry.get("namen", []):
                if name not in template_names:
                    continue
                names.setdefault(name, entry["bild"])
    made = 0
    for fig in FIGURES:
        for bild, count in sorted(images.items()):
            for n in range(count):
                src = source / fig / bild / f"{n}.jpg"
                if not src.exists():
                    raise SystemExit(f"Fehlt: {src}")
                dst = out_dir / fig / bild / f"{n}.jpg"
                if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(
                    ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(QUALITY), "-Z", str(SIZE),
                     str(src), "--out", str(dst)],
                    check=True, capture_output=True,
                )
                made += 1
        # Übrig gebliebene Ordner (Bild nicht mehr in der Zuordnung) entfernen
        for folder in (out_dir / fig).iterdir():
            if folder.is_dir() and folder.name not in images:
                shutil.rmtree(folder)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps({"exercises": exercises, "names": dict(sorted(names.items())), "images": dict(sorted(images.items()))},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"{len(exercises)} Übungen aus Vorlagen, {len(images)} Bilder je Figur, {made} Dateien neu → {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="Pfad zum Bilder-Repo (mit zuordnung.json, m/, w/)")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--out-json", type=Path, default=OUT_JSON)
    parser.add_argument("--plans", type=Path, default=PLANS, help="Ordner mit den mitgelieferten Vorlagen")
    args = parser.parse_args()
    build(args.source.resolve(), args.out_dir, args.out_json, args.plans)
