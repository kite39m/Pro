import httpx
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class SearchWebInput(BaseModel):
    query: str = Field(description="搜索关键词")
    num_results: int = Field(default=10, description="返回结果数量")


class SearchWebTool(BaseTool):
    name: str = "search_web"
    description: str = "通过搜索引擎搜索网页信息，返回标题、URL、摘要"
    args_schema: Type[BaseModel] = SearchWebInput
    api_key: str = ""

    async def _arun(self, query: str, num_results: int = 10) -> list[dict]:
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

    def _run(self, query: str, num_results: int = 10) -> list[dict]:
        raise NotImplementedError("Use async version")
