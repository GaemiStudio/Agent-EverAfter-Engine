from google.adk.agents import Agent

root_agent = Agent (
    name="basic_agent",
    model="gemini-2.5-flash-lite",
    description="Basic agent",
    instruction="""
    You are a basic assistant that will help the user with any questions.
    """,
)