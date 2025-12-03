from datetime import datetime
from typing import Any, Dict, List, Optional, Annotated
from enum import Enum
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage


# Enum definitions
class ResearchStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Type definitions
class ResearchQuestion(BaseModel):
    question: str
    context: Optional[str] = None


class SubQuestion(BaseModel):
    question: str
    parent_question: Optional[str] = None


class Source(BaseModel):
    id: str
    url: str
    title: Optional[str] = None
    relevance_score: Optional[float] = None


class Passage(BaseModel):
    id: str
    source_id: str
    content: str
    page_num: Optional[int] = None


class ResearchReport(BaseModel):
    question: str
    summary: str
    findings: List[str]
    sources: List[Source]
    generated_at: str


class ResearchState(BaseModel):
    # Input
    research_question: Optional[ResearchQuestion] = None

    # Intermediate states
    sub_questions: List[SubQuestion] = Field(default_factory=list)
    search_queries: List[str] = Field(default_factory=list)
    sources: List[Source] = Field(default_factory=list)
    passages: List[Passage] = Field(default_factory=list)

    # Final output
    research_report: Optional[ResearchReport] = None

    # Processing metadata
    status: ResearchStatus = ResearchStatus.PENDING
    current_step: str = "initialized"
    error_message: Optional[str] = None
    processing_stats: Dict[str, Any] = Field(default_factory=dict)
    
# Node base class
class GraphNode:
    """Base class for graph nodes"""
    def __init__(self, llm: Optional[BaseLanguageModel] = None, crawler: Optional[Any] = None):
        self.llm = llm
        self.crawler = crawler
    
    def _report_progress(self, message: str, step: str) -> None:
        """Report progress during processing"""
        print(f"[{step.upper()}] {message}")


class PlannerNode(GraphNode):
    async def plan(self, state: ResearchState) -> ResearchState:
        self._report_progress("Analyzing research question", "planning")
        
        # Generate sub-questions
        if state.research_question:
            sub_questions = await self._decompose_question(state.research_question)
            state.sub_questions = sub_questions
        
        self._report_progress(f"Generated {len(state.sub_questions)} sub-questions", "planning")
        return state
        
    async def _decompose_question(self, research_question: ResearchQuestion) -> List[SubQuestion]:
        current_date = datetime.now().strftime("%B %Y")  # "August 2025"
        
        system_prompt = f"""You are a research planning expert. 
        Current date: {current_date}
        
        Decompose this research question into 3-7 focused sub-questions that together 
        will comprehensively answer the main question. If the question asks for 
        "latest" or "recent" information, focus on finding up-to-date content."""
        
        if self.llm:
            response = await self.llm.ainvoke([{"type": "system", "content": system_prompt}, 
                                              {"type": "human", "content": research_question.question}])
        
        # Placeholder for parsing logic to create SubQuestion objects
        return []
class FetcherNode(GraphNode):
    async def fetch(self, state: ResearchState) -> ResearchState:
        self._report_progress("Starting content extraction", "fetching")
        
        all_passages = []
        for source in state.sources:
            try:
                # Extract clean content using Crawl4AI
                if self.crawler:
                    result = await self.crawler.arun(
                        url=str(source.url),
                        word_count_threshold=10,
                        exclude_tags=['nav', 'footer', 'aside', 'header'],
                        remove_overlay_elements=True,
                    )
                    
                    if result.success and result.markdown:
                        # Split content into manageable passages
                        passages = self._split_into_passages(result.markdown, source.id)
                        all_passages.extend(passages)
            except Exception:
                continue  # Skip failed sources
        
        state.passages = all_passages
        return state
    
    def _split_into_passages(self, content: str, source_id: str, chunk_size: int = 1000) -> List[Passage]:
        """Split content into manageable passage chunks"""
        passages = []
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        for idx, chunk in enumerate(chunks):
            passage = Passage(
                id=f"{source_id}_chunk_{idx}",
                source_id=source_id,
                content=chunk,
                page_num=idx
            )
            passages.append(passage)
        
        return passages