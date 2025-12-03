from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A debugger agent for testing code snippets and finding errors.',
    instruction='Answer user questions to the best of your knowledge',
)
