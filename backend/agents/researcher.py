import asyncio
from agents.state import ResearchState, Finding, Source
from tools.search import SearchWebTool
from tools.crawler import CrawlPageTool
from config import get_settings
from utils.text import deduplicate_findings


async def researcher_node(state: ResearchState) -> dict:
    """并发搜索所有子任务，采集原始数据"""
    settings = get_settings()
    search_tool = SearchWebTool(api_key=settings.serpapi_api_key)
    crawl_tool = CrawlPageTool(timeout=settings.crawler_timeout)

    sub_tasks = state["sub_tasks"]
    revision_queries = state.get("revision_queries", [])

    all_findings: list[Finding] = []
    all_sources: list[Source] = []

    async def search_subtask(task: dict) -> list[Finding]:
        findings = []
        # 每个子任务只取前2个关键词（中英各1），减少搜索次数
        keywords = (task.get("search_keywords_zh", []) + task.get("search_keywords_en", []))[:2]

        for keyword in keywords:
            try:
                results = await search_tool._arun(keyword, num_results=5)
                for r in results:
                    findings.append({
                        "content": r.get("snippet", ""),
                        "source_url": r.get("url", ""),
                        "source_type": "news",
                        "relevance_score": 0.5,
                    })
                    all_sources.append({
                        "url": r.get("url", ""),
                        "title": r.get("title", ""),
                        "date": r.get("date", ""),
                        "snippet": r.get("snippet", ""),
                    })
            except Exception:
                continue
        return findings

    async def search_revision(query: str) -> list[Finding]:
        try:
            results = await search_tool._arun(query, num_results=5)
            findings = []
            for r in results:
                findings.append({
                    "content": r.get("snippet", ""),
                    "source_url": r.get("url", ""),
                    "source_type": "news",
                    "relevance_score": 0.5,
                })
                all_sources.append({
                    "url": r.get("url", ""),
                    "title": r.get("title", ""),
                    "date": r.get("date", ""),
                    "snippet": r.get("snippet", ""),
                })
            return findings
        except Exception:
            return []

    if revision_queries:
        tasks = [search_revision(q) for q in revision_queries]
    else:
        tasks = [search_subtask(task) for task in sub_tasks]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, list):
            all_findings.extend(result)

    all_findings = deduplicate_findings(all_findings)
    all_sources = deduplicate_findings(all_sources)

    return {
        "raw_findings": all_findings,
        "sources": all_sources,
        "status": "researched",
    }
