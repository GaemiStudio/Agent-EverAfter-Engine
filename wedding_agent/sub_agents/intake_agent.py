# agents/intake_agent/agent.py

import asyncio
import json

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from shared.memory_manager import (
    save_wedding_state,
    append_notes,
    build_intake_summary,
)

APP_NAME = "wedding_planner_app"
USER_ID = "intake_user"
SESSION_ID = "intake_session"

INSTRUCTION = """
You are the intake specialist for a wedding planning AI system.

Your job:
- Read the user's message, which contains everything the couple told you about their wedding.
- Extract the information and output a SINGLE JSON object that follows EXACTLY this schema:

{
  "couple": {
    "partner1_name": "string",
    "partner2_name": "string",
    "pronouns": "string",
    "contact_email": "string"
  },
  "event": {
    "date": "string",               // ISO-like date: e.g. "2026-05-14"
    "city": "string",
    "estimated_guests": 0,
    "ceremony_style": "string",
    "reception_style": "string"
  },
  "preferences": {
    "overall_vibe": "string",
    "colors": ["string"],
    "must_haves": ["string"],
    "dealbreakers": ["string"]
  },
  "constraints": {
    "budget_total": 0,
    "hard_end_time": "string",      // e.g. "22:00"
    "accessibility_needs": "string"
  }
}

Rules:
- If the couple didn't provide something, make your best reasonable guess or leave it as an empty string, 0, or [].
- RETURN ONLY THE JSON. No extra text, no explanation, no backticks.
- Make sure it is valid JSON: double quotes, commas, etc.
"""

# ADK Agent definition
intake_agent = Agent(
    name="intake_agent",
    model="gemini-2.5-flash",  # or "gemini-2.5-flash-lite" etc.
    description="Collects and structures core wedding details.",
    instruction=INSTRUCTION,
)

# Simple in-memory runner for local use
_session_service = InMemorySessionService()
_runner = InMemoryRunner(agent=intake_agent, app_name=APP_NAME)


async def _ensure_session():
    # Create a single session we can reuse for this intake agent.
    await _session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

# Create the session at import time (fine for a simple local script)
asyncio.run(_ensure_session())


def run_intake_and_save(couple_answers: str) -> dict:
    """
    High-level helper:

    1. Send the couple's raw answers to the intake_agent.
    2. Parse the JSON response into a Python dict.
    3. Save to wedding_state.json.
    4. Append a human summary to wedding_notes.txt.
    5. Return the state dict.
    """

    # Prepare the user's message in ADK format
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=couple_answers)],
    )

    final_text = ""

    # Synchronous wrapper over runner.run() so you can call this from normal code.
    for event in _runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        # We only care about final text content coming back from the agent.
        if (
            event.content
            and event.content.parts
            and event.content.parts[0].text
        ):
            final_text = event.content.parts[0].text.strip()

    if not final_text:
        raise RuntimeError("IntakeAgent did not return any text response.")

    # Now parse the JSON
    try:
        state = json.loads(final_text)
    except json.JSONDecodeError as e:
        # Helpful error if Gemini sneaks in extra text
        raise ValueError(
            f"IntakeAgent produced invalid JSON: {e}\n\nRaw output:\n{final_text}"
        )

    # Persist core state
    save_wedding_state(state)

    # Append a human-readable summary to the notes file
    summary = build_intake_summary(state)
    append_notes("Intake Summary", summary)

    return state
