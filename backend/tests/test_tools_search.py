import pytest
from unittest.mock import AsyncMock, patch
from tools.search import SearchWebTool


@pytest.mark.asyncio
async def test_search_web_returns_results():
    tool = SearchWebTool(api_key="test_key")

    mock_response = {
        "organic_results": [
            {
                "title": "Test Title",
                "link": "https://example.com",
                "snippet": "Test snippet",
                "date": "2026-01-01",
            }
        ]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = AsyncMock(
            json=lambda: mock_response,
            status_code=200,
            raise_for_status=lambda: None,
        )
        results = await tool._arun("test query", num_results=5)

    assert len(results) == 1
    assert results[0]["title"] == "Test Title"
    assert results[0]["url"] == "https://example.com"


@pytest.mark.asyncio
async def test_search_web_empty_results():
    tool = SearchWebTool(api_key="test_key")

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = AsyncMock(
            json=lambda: {"organic_results": []},
            status_code=200,
            raise_for_status=lambda: None,
        )
        results = await tool._arun("no results query")

    assert results == []
