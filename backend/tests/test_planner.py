import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.planner import planner_node
from agents.state import ResearchState


@pytest.mark.asyncio
async def test_planner_produces_sub_tasks():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = '''
    {
        "sub_tasks": [
            {
                "topic": "核心零部件供应链",
                "search_keywords_zh": ["人形机器人 减速器"],
                "search_keywords_en": ["humanoid robot actuator"],
                "priority": "high"
            },
            {
                "topic": "头部企业融资",
                "search_keywords_zh": ["人形机器人 融资 2026"],
                "search_keywords_en": ["humanoid robot funding 2026"],
                "priority": "medium"
            }
        ]
    }
    '''
    mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    state: ResearchState = {
        "user_query": "分析 2026 Q1 全球人形机器人市场格局",
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

    with patch("agents.planner.get_llm_router") as mock_router:
        mock_router.return_value.get_llm.return_value = mock_llm
        result = await planner_node(state)

    assert len(result["sub_tasks"]) == 2
    assert result["sub_tasks"][0]["topic"] == "核心零部件供应链"
    assert result["status"] == "planned"
