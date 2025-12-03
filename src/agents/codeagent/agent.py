from google.adk.agents import SequentialAgent
from marialuisa.agent import root_agent as marialuisa_agent
from eugenio.agent import root_agent as eugenio_agent
from walter.agent import root_agent as walter_agent

code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[
        marialuisa_agent,
        eugenio_agent,
        walter_agent,
    ],
    description="""An orchestrator agent that coordinates the planning, building, and testing of deep learning models based on user specifications.""",
)

root_agent = code_pipeline_agent