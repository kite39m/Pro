import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from utils.text import clean_html_text, truncate_text


class CrawlPageInput(BaseModel):
    url: str = Field(description="要抓取的网页 URL")


class CrawlPageTool(BaseTool):
    name: str = "crawl_page"
    description: str = "抓取指定 URL 的网页内容，返回清洗后的正文文本"
    args_schema: Type[BaseModel] = CrawlPageInput
    timeout: int = 10
    max_content_bytes: int = 50000

    USER_AGENTS: list[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]

    async def _arun(self, url: str) -> str:
        import random
        headers = {"User-Agent": random.choice(self.USER_AGENTS)}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers, follow_redirects=True)
                resp.raise_for_status()
                html = resp.text
        except (httpx.TimeoutException, httpx.HTTPError):
            return ""

        soup = BeautifulSoup(html, "lxml")

        # 移除无用标签
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # 尝试用 readability 提取正文
        try:
            from readability import Document
            doc = Document(html)
            content = clean_html_text(doc.summary())
        except Exception:
            content = clean_html_text(soup.get_text())

        return truncate_text(content, self.max_content_bytes)

    def _run(self, url: str) -> str:
        raise NotImplementedError("Use async version")
