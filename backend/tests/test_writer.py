import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.writer import writer_node
from agents.state import ResearchState


@pytest.mark.asyncio
async def test_writer_produces_final_report():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = """# 2026 Q1 全球人形机器人市场格局分析

## 执行摘要
本报告基于多源公开数据，对2026年第一季度全球人形机器人市场进行了全面分析。

## 一、市场概览
市场规模持续扩大...

## 数据来源
1. [Example Report](https://example.com)
"""
    mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    state: ResearchState = {
        "user_query": "分析 2026 Q1 全球人形机器人市场格局",
        "sub_tasks": [],
        "raw_findings": [],
        "insights": [],
        "draft_report": "# 草稿...",
        "critique": "无问题",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [{"url": "https://example.com", "title": "Example", "date": "2026", "snippet": "test"}],
        "status": "criticized",
    }

    with patch("agents.writer.get_llm_router") as mock_router:
        mock_router.return_value.get_llm.return_value = mock_llm
        result = await writer_node(state)

    assert result["final_report"] != ""
    assert "人形机器人" in result["final_report"]
    assert result["status"] == "completed"
