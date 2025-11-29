import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

STATE_PATH = DATA_DIR / "wedding_state.json"
NOTES_PATH = DATA_DIR / "wedding_notes.txt"


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def append_notes(section_title: str, content: str) -> None:
    """Append a section to wedding_notes.txt with a timestamp and header."""
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    header = f"\n\n=== {section_title.upper()} ===\n[{timestamp}]\n"
    with open(NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(content.strip())
        f.write("\n")
