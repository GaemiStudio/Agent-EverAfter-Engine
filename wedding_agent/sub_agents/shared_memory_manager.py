# shared/memory_manager.py

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

# Base paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

WEDDING_STATE_PATH = DATA_DIR / "wedding_state.json"
WEDDING_NOTES_PATH = DATA_DIR / "wedding_notes.txt"


# ---- Default schema for new weddings ---------------------------------------

DEFAULT_WEDDING_STATE: Dict[str, Any] = {
    "couple": {
        "partner1_name": "",
        "partner2_name": "",
        "pronouns": "",
        "contact_email": "",
    },
    "event": {
        "date": "",              # ISO date string, e.g. "2026-05-14"
        "city": "",
        "estimated_guests": 0,
        "ceremony_style": "",
        "reception_style": "",
    },
    "preferences": {
        "overall_vibe": "",
        "colors": [],
        "must_haves": [],
        "dealbreakers": [],
    },
    "constraints": {
        "budget_total": 0,
        "hard_end_time": "",     # e.g. "22:00"
        "accessibility_needs": "",
    },
}


# ---- Core helpers -----------------------------------------------------------

def load_wedding_state() -> Dict[str, Any]:
    """Load the current wedding_state.json, or return a default structure."""
    if not WEDDING_STATE_PATH.exists():
        # First run: write a default file so other code can rely on its existence.
        save_wedding_state(DEFAULT_WEDDING_STATE)
        return DEFAULT_WEDDING_STATE.copy()

    with open(WEDDING_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_wedding_state(state: Dict[str, Any]) -> None:
    """Overwrite wedding_state.json with the given dict."""
    with open(WEDDING_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def append_notes(section_title: str, content: str) -> None:
    """
    Append a labeled section to wedding_notes.txt.

    The file is automatically created if it doesn't exist.
    """
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    header = f"\n\n=== {section_title.upper()} ===\n[{timestamp}]\n"

    with open(WEDDING_NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(content.strip())
        f.write("\n")


# ---- Optional: pretty human-readable summary for intake ---------------------

def build_intake_summary(state: Dict[str, Any]) -> str:
    """Create a short human-readable summary of the intake JSON."""
    couple = state.get("couple", {})
    event = state.get("event", {})
    prefs = state.get("preferences", {})
    constraints = state.get("constraints", {})

    lines = [
        f"Couple: {couple.get('partner1_name', '').strip()} & {couple.get('partner2_name', '').strip()}",
        f"Pronouns: {couple.get('pronouns', '')}",
        f"Contact: {couple.get('contact_email', '')}",
        "",
        f"Date / Location: {event.get('date', '')} in {event.get('city', '')}",
        f"Guests: {event.get('estimated_guests', 0)}",
        f"Ceremony style: {event.get('ceremony_style', '')}",
        f"Reception style: {event.get('reception_style', '')}",
        "",
        f"Overall vibe: {prefs.get('overall_vibe', '')}",
        f"Colors: {', '.join(prefs.get('colors', []))}",
        f"Must-haves: {', '.join(prefs.get('must_haves', []))}",
        f"Dealbreakers: {', '.join(prefs.get('dealbreakers', []))}",
        "",
        f"Total budget: {constraints.get('budget_total', 0)}",
        f"Hard end time: {constraints.get('hard_end_time', '')}",
        f"Accessibility: {constraints.get('accessibility_needs', '')}",
    ]

    return "\n".join(lines)

