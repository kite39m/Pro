import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.synthesizer import synthesizer_node
from agents.state import ResearchState


@pytest.mark.asyncio
async def test_synthesizer_produces_insights_and_draft():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = """# 人形机器人市场分析

## 执行摘要
2026年Q1人形机器人市场呈现快速增长态势。

## 关键洞察
1. 减速器供应链集中度提升
2. 头部企业融资加速

## 详细分析
基于多源数据分析..."""
    mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    state: ResearchState = {
        "user_query": "人形机器人市场",
        "sub_tasks": [{"topic": "供应链", "search_keywords_zh": [], "search_keywords_en": [], "priority": "high"}],
        "raw_findings": [
            {"content": "减速器市场增长", "source_url": "https://example.com", "source_type": "news", "relevance_score": 0.8}
        ],
        "insights": [],
        "draft_report": "",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [{"url": "https://example.com", "title": "Test", "date": "2026", "snippet": "test"}],
        "status": "researched",
    }

    with patch("agents.synthesizer.get_llm_router") as mock_router:
        mock_router.return_value.get_llm.return_value = mock_llm
        result = await synthesizer_node(state)

    assert result["draft_report"] != ""
    assert "人形机器人" in result["draft_report"]
    assert result["status"] == "synthesized"
    assert len(result["insights"]) > 0
