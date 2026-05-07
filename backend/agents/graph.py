from langgraph.graph import StateGraph, START, END
from agents.state import ResearchState
from agents.planner import planner_node
from agents.researcher import researcher_node
from agents.synthesizer import synthesizer_node
from agents.critic import critic_node
from agents.writer import writer_node


def build_graph() -> StateGraph:
    """构建 LangGraph 状态机"""
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_node("critic", critic_node)
    graph.add_node("writer", writer_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "synthesizer")
    graph.add_edge("synthesizer", "critic")

    graph.add_conditional_edges(
        "critic",
        lambda state: "writer" if not state["needs_revision"] else "researcher",
        {"writer": "writer", "researcher": "researcher"},
    )

    graph.add_edge("writer", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
