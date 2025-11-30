from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent (
    name="wedding_agent",
    model="gemini-2.5-flash-lite",
    description="wedding agent",
    instruction="""

    You are a helpful personal assistant that is responsible for overseeing the work of the other agents. 
    Your primary goal is to maintain the Shared Context Object, delegate tasks efficiently, and ensure the 
    final Consolidated Plan adheres to all user constraints (budget, date, guest count).

    Always delegate the task to the appropriate agent. Use your best judgement to determine which agent to delegate to.

    You are responsible for delegating tasks to the following specialized agents:

        - Intake Agent: Ask core questions, gather all inputs needed to plan wedding into a clean structured JSON object that other agents can use.


    You also have access to the following tools for information gathering:

        - Google Search: For current vendor information, local cost estimates, and trend research.

        
    """,
    sub_agents=[
        budget_agent,
        catering_agent,
        creative_agent,
        intake_agent,
        photography_agent,
        shared_memory_manager
        
    ],
    tools=[google_search],
)
