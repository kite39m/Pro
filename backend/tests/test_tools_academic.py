import httpx
import pytest
from unittest.mock import AsyncMock, patch
from tools.academic import SearchAcademicTool


@pytest.mark.asyncio
async def test_search_academic_returns_results():
    tool = SearchAcademicTool()

    mock_response = {
        "data": [
            {
                "title": "Robot Learning Paper",
                "url": "https://arxiv.org/abs/12345",
                "abstract": "We propose a new method for robot learning.",
                "year": 2026,
                "authors": [{"name": "Alice"}, {"name": "Bob"}],
            }
        ]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = AsyncMock(
            json=lambda: mock_response,
            status_code=200,
            raise_for_status=lambda: None,
        )
        results = await tool._arun("robot learning")

    assert len(results) == 1
    assert results[0]["title"] == "Robot Learning Paper"
    assert results[0]["source_type"] == "academic"


@pytest.mark.asyncio
async def test_search_academic_empty_on_error():
    tool = SearchAcademicTool()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.TimeoutException("timeout")
        results = await tool._arun("query")

    assert results == []
