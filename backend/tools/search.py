import asyncio
import random
import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import ClassVar, Type


class SearchWebInput(BaseModel):
    query: str = Field(description="搜索关键词")
    num_results: int = Field(default=10, description="返回结果数量")


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]


class SearchWebTool(BaseTool):
    name: str = "search_web"
    description: str = "通过搜索引擎搜索网页信息，返回标题、URL、摘要"
    args_schema: Type[BaseModel] = SearchWebInput
    api_key: str = ""

    async def _arun(self, query: str, num_results: int = 10) -> list[dict]:
        # 优先使用 SerpAPI
        if self.api_key and self.api_key != "your_serpapi_key":
            return await self._search_serpapi(query, num_results)
        # 回退到 DuckDuckGo HTML 爬取
        return await self._search_ddg_html(query, num_results)

    async def _search_serpapi(self, query: str, num_results: int) -> list[dict]:
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": num_results,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get("https://serpapi.com/search", params=params)
            resp.raise_for_status()
            data = resp.json()

        results = []
        for item in data.get("organic_results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "date": item.get("date", ""),
            })
        return results

    async def _search_ddg_html(self, query: str, num_results: int) -> list[dict]:
        """通过 DuckDuckGo HTML 版搜索，无需 API key"""
        import random
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        url = "https://html.duckduckgo.com/html/"
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                resp = await client.post(url, data={"q": query}, headers=headers)
                resp.raise_for_status()
                html = resp.text
        except Exception:
            return []

        soup = BeautifulSoup(html, "lxml")
        results = []

        # DuckDuckGo HTML 结果在 class="result" 的 div 中
        for item in soup.select(".result"):
            title_tag = item.select_one(".result__a")
            snippet_tag = item.select_one(".result__snippet")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

            # DuckDuckGo 的链接可能是重定向 URL，提取真实 URL
            if "uddg=" in href:
                from urllib.parse import unquote, parse_qs, urlparse
                parsed = urlparse(href)
                actual = parse_qs(parsed.query).get("uddg", [""])[0]
                href = unquote(actual) if actual else href

            results.append({
                "title": title,
                "url": href,
                "snippet": snippet,
                "date": "",
            })

            if len(results) >= num_results:
                break

        return results

    def _run(self, query: str, num_results: int = 10) -> list[dict]:
        raise NotImplementedError("Use async version")
