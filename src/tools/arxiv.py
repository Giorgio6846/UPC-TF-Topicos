# research_pipeline_adk.py

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, AsyncGenerator

from pydantic import BaseModel, Field
from typing_extensions import override

# ADK imports
from google.adk.agents import LlmAgent, SequentialAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types


# -------------------------------------------------------------------
# 1. Domain models (como en tu código original)
# -------------------------------------------------------------------

# Suponiendo que ya tienes estos modelos definidos en tu código.
# Aquí los dejo como "placeholders" mínimos para que el fichero sea auto-contenible.
class ResearchQuestion(BaseModel):
    text: str


class SubQuestion(BaseModel):
    id: str
    text: str


class Source(BaseModel):
    id: str
    url: str
    title: Optional[str] = None
    snippet: Optional[str] = None


class ResearchReport(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResearchStatus(str):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    ERROR = "ERROR"


class ResearchState(BaseModel):
    # Input
    research_question: Optional[ResearchQuestion] = None

    # Intermediate states
    sub_questions: List[SubQuestion] = Field(default_factory=list)
    search_queries: List[str] = Field(default_factory=list)
    sources: List[Source] = Field(default_factory=list)
    passages: List[Dict[str, Any]] = Field(default_factory=list)

    # Final output
    research_report: Optional[ResearchReport] = None

    # Processing metadata
    status: ResearchStatus = ResearchStatus.PENDING
    current_step: str = "initialized"
    error_message: Optional[str] = None
    processing_stats: Dict[str, Any] = Field(default_factory=dict)


# -------------------------------------------------------------------
# 2. Helpers para mapear entre ADK session.state y ResearchState
# -------------------------------------------------------------------

STATE_KEY = "research_state"


def get_research_state(ctx: InvocationContext) -> ResearchState:
    raw = ctx.session.state.get(STATE_KEY)
    if raw is None:
        # Inicializa un estado vacío si no existe
        state = ResearchState()
        ctx.session.state[STATE_KEY] = state.model_dump()
        return state
    return ResearchState.model_validate(raw)


def set_research_state(ctx: InvocationContext, state: ResearchState) -> None:
    ctx.session.state[STATE_KEY] = state.model_dump()


# -------------------------------------------------------------------
# 3. Planner: LlmAgent que sustituye a PlannerNode + decompose_question
# -------------------------------------------------------------------

class PlannerOutput(BaseModel):
    sub_questions: List[SubQuestion]


def build_planner_agent(model_name: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Agent que descompone la pregunta de investigación en sub-preguntas.
    Usa ADK, no langgraph.
    """
    # Notar que usamos variables de estado {research_question_text} y {current_date}
    # que deberás rellenar en session.state antes de ejecutar.
    instruction = """
You are a research planning expert.

Current date: {current_date}

Main research question:
{research_question_text}

Decompose this research question into 3-7 focused sub-questions that together
will comprehensively answer the main question.

Return ONLY valid JSON matching this schema:

{
  "sub_questions": [
    {
      "id": "short-stable-id",
      "text": "The text of the sub-question"
    },
    ...
  ]
}
"""

    return LlmAgent(
        model=model_name,
        name="planner",
        description="Decomposes a research question into focused sub-questions.",
        instruction=instruction,
        output_schema=PlannerOutput,
        # Guardamos el JSON (como texto) en session.state["planner_raw_output"]
        output_key="planner_raw_output",
        include_contents="none",
    )


# -------------------------------------------------------------------
# 4. Searcher, Ranker, Writer como LlmAgents (esqueletos)
# -------------------------------------------------------------------

class SearcherOutput(BaseModel):
    search_queries: List[str]
    sources: List[Source]


def build_searcher_agent(model_name: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Toma sub-preguntas y genera queries + fuentes candidate.
    """
    instruction = """
You are a web research search expert.

You are given JSON with sub-questions in the state key `planner_raw_output`.
Parse it and propose:

- A
