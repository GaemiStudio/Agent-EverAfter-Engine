from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# Import shared memory helpers
from shared.memory_manager import load_wedding_state, append_notes


# ------------------------
# 1) Creative Agent definition
# ------------------------

creative_agent = Agent(
    name="creative_agent",
    model="gemini-2.0-flash",
    description="Handles all personalized text content including vows, speeches, and scripts for the wedding.",
    instruction="""
    You are the Creative Agent, a skilled writer specializing in heartfelt, personalized wedding content.

    Your responsibilities:
    - Write personalized wedding vows that reflect the couple's unique love story
    - Craft speeches for the best man, maid of honor, and other wedding party members
    - Create ceremony scripts tailored to the couple's style (traditional, modern, humorous, etc.)
    - Write toasts, readings, and other ceremonial text
    - Help with save-the-date and invitation wording

    When writing content:
    1. Always ask about the couple's story, how they met, and meaningful moments
    2. Understand their preferred tone (romantic, funny, heartfelt, formal)
    3. Incorporate personal details, inside jokes, or shared experiences when provided
    4. Offer multiple drafts or variations when appropriate

    Draw from your knowledge of:
    - Famous wedding vows and speeches for inspiration
    - Poetry, quotes, and literary references
    - Cultural and religious traditions
    """,
)


# ------------------------
# 2) Runner + session setup
# ------------------------

APP_NAME = "wedding_planner_app"
USER_ID = "creative_user"
SESSION_ID = "creative_session"

_session_service = InMemorySessionService()
_runner = InMemoryRunner(agent=creative_agent, app_name=APP_NAME)

async def _ensure_session():
    await _session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

asyncio.run(_ensure_session())


# ------------------------
# 3) Public run function
# ------------------------

def run_creative():
    """
    Loads the shared wedding state, sends it to the Creative Agent,
    gets Gemini's response, appends it to wedding_notes.txt, and
    returns the text.
    """
    # Load the current wedding state JSON
    state = load_wedding_state()

    # Prepare message for the agent
    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Here is the wedding state:\n"
                    f"{state}\n\n"
                    "Based on this, generate creative wedding text "
                    "(vows, ceremony script, or speech suggestions) that fits the couple's style."
                )
            )
        ],
    )

    final_text = ""

    # Run agent
    for event in _runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            final_text = event.content.parts[0].text.strip()

    # Append to wedding_notes.txt
    append_notes("Creative Writing Output", final_text)

    return final_text
