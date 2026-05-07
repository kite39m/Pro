import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.critic import critic_node
from agents.state import ResearchState


@pytest.mark.asyncio
async def test_critic_approves_good_report():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = '''
    {
        "needs_revision": false,
        "critique": "报告质量良好，论点有数据支撑。",
        "revision_queries": []
    }
    '''
    mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    state: ResearchState = {
        "user_query": "test",
        "sub_tasks": [],
        "raw_findings": [],
        "insights": [],
        "draft_report": "# 好报告\n\n有数据支撑的分析...",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [],
        "status": "synthesized",
    }

    with patch("agents.critic.get_llm_router") as mock_router:
        mock_router.return_value.get_llm.return_value = mock_llm
        result = await critic_node(state)

    assert result["needs_revision"] is False
    assert result["status"] == "criticized"


@pytest.mark.asyncio
async def test_critic_requests_revision():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = '''
    {
        "needs_revision": true,
        "critique": "第三段缺乏数据支撑，需要补充减速器市场份额数据。",
        "revision_queries": ["减速器 市场份额 2026", "harmonic drive market share"]
    }
    '''
    mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    state: ResearchState = {
        "user_query": "test",
        "sub_tasks": [],
        "raw_findings": [],
        "insights": [],
        "draft_report": "# 草稿报告...",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [],
        "status": "synthesized",
    }

    with patch("agents.critic.get_llm_router") as mock_router:
        mock_router.return_value.get_llm.return_value = mock_llm
        result = await critic_node(state)

    assert result["needs_revision"] is True
    assert len(result["revision_queries"]) == 2
