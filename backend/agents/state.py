from typing import TypedDict, Annotated
from operator import add


class SubTask(TypedDict):
    topic: str
    search_keywords_zh: list[str]
    search_keywords_en: list[str]
    priority: str  # "high" | "medium" | "low"


class Finding(TypedDict):
    content: str
    source_url: str
    source_type: str  # "news" | "report" | "social" | "academic"
    relevance_score: float


class Insight(TypedDict):
    title: str
    reasoning: str
    supporting_finding_indices: list[int]


class Source(TypedDict):
    url: str
    title: str
    date: str
    snippet: str


class ResearchState(TypedDict):
    # 用户输入
    user_query: str
    # Planner 输出
    sub_tasks: list[SubTask]
    # Researcher 输出
    raw_findings: Annotated[list[Finding], add]
    # Synthesizer 输出
    insights: list[Insight]
    draft_report: str
    # Critic 输出
    critique: str
    needs_revision: bool
    revision_queries: list[str]
    # Writer 输出
    final_report: str
    # 元数据
    sources: list[Source]
    status: str
