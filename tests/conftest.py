"""Tests für die reine Logik (ohne laufendes Home Assistant)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
