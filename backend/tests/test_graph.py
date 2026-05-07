import pytest
from agents.graph import build_graph


def test_graph_has_all_nodes():
    graph = build_graph()
    node_names = list(graph.get_graph().nodes.keys())
    assert "planner" in node_names
    assert "researcher" in node_names
    assert "synthesizer" in node_names
    assert "critic" in node_names
    assert "writer" in node_names


def test_graph_structure():
    graph = build_graph()
    assert graph is not None
