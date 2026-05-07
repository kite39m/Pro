import pytest
import httpx
from unittest.mock import AsyncMock, patch
from tools.crawler import CrawlPageTool


@pytest.mark.asyncio
async def test_crawl_page_extracts_text():
    tool = CrawlPageTool()

    html = """
    <html>
    <head><title>Test</title></head>
    <body>
        <nav>Navigation</nav>
        <article>
            <h1>Article Title</h1>
            <p>This is the main content of the article.</p>
        </article>
        <footer>Footer</footer>
    </body>
    </html>
    """

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = AsyncMock(
            text=html,
            status_code=200,
            raise_for_status=lambda: None,
        )
        result = await tool._arun("https://example.com")

    assert "Article Title" in result
    assert "main content" in result


@pytest.mark.asyncio
async def test_crawl_page_timeout_returns_empty():
    tool = CrawlPageTool()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.TimeoutException("timeout")
        result = await tool._arun("https://slow-site.com")

    assert result == ""
