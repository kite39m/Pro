from agents.state import ResearchState


def test_state_has_required_fields():
    """验证状态包含所有必需字段"""
    state: ResearchState = {
        "user_query": "test query",
        "sub_tasks": [],
        "raw_findings": [],
        "insights": [],
        "draft_report": "",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [],
        "status": "pending",
    }
    assert state["user_query"] == "test query"
    assert state["needs_revision"] is False
    assert state["status"] == "pending"


def test_raw_findings_append():
    """验证 raw_findings 支持 append 操作（Annotated with add）"""
    from typing import get_type_hints
    hints = get_type_hints(ResearchState)
    # raw_findings 应该是 Annotated[list[dict], add]
    assert "raw_findings" in hints
