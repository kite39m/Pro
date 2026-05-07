import pytest
from unittest.mock import AsyncMock, patch
from agents.researcher import researcher_node
from agents.state import ResearchState


@pytest.mark.asyncio
async def test_researcher_collects_findings():
    state: ResearchState = {
        "user_query": "人形机器人市场",
        "sub_tasks": [
            {
                "topic": "供应链",
                "search_keywords_zh": ["人形机器人 减速器"],
                "search_keywords_en": ["humanoid robot actuator"],
                "priority": "high",
            }
        ],
        "raw_findings": [],
        "insights": [],
        "draft_report": "",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [],
        "status": "planned",
    }

    mock_search_results = [
        {"title": "减速器市场报告", "url": "https://example.com/1", "snippet": "2026年减速器...", "date": "2026-01"},
        {"title": "Actuator Report", "url": "https://example.com/2", "snippet": "Actuator market...", "date": "2026-01"},
    ]

    with patch("agents.researcher.SearchWebTool") as MockSearch:
        mock_tool = MockSearch.return_value
        mock_tool._arun = AsyncMock(return_value=mock_search_results)
        result = await researcher_node(state)

    assert len(result["raw_findings"]) > 0
    assert result["status"] == "researched"
    assert len(result["sources"]) > 0
