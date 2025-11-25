from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent (
    name="personal_assistant",
    model="gemini-2.5-flash-lite",
    description="personal assistant agent",
    instruction="""

    You are a helpful personal assistant that is responsible for overseeing
    the work of the other agents.
    
    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    -TBD
    -TBD
    -TBD

    You also have access to the following tools:
    -TBD
    -TBD
    -TBD

    """,
    sub_agents=[],
    tools=[google_search],
)
