from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import ResearchState
from models.llm import get_llm_router


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "synthesizer.md"


async def synthesizer_node(state: ResearchState) -> dict:
    """综合分析原始发现，进行逻辑推演，生成草稿报告"""
    router = get_llm_router()
    llm = router.get_llm("synthesizer")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    findings_text = ""
    for i, f in enumerate(state["raw_findings"][:50], 1):
        findings_text += f"[{i}] {f['content']} (来源: {f['source_url']})\n"

    sources_text = ""
    for i, s in enumerate(state["sources"][:30], 1):
        sources_text += f"[{i}] {s['title']} - {s['url']}\n"

    human_message = f"""## 研究议题
{state['user_query']}

## 子任务
{', '.join(t['topic'] for t in state['sub_tasks'])}

## 原始发现
{findings_text}

## 来源列表
{sources_text}

请基于以上信息进行综合分析，输出草稿报告。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_message),
    ]

    response = await llm.ainvoke(messages)
    draft = response.content

    insights = []
    for line in draft.split("\n"):
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "4.", "5.", "-", "•")) and len(line) > 10:
            insights.append({
                "title": line.lstrip("0123456789.-• "),
                "reasoning": "",
                "supporting_finding_indices": [],
            })

    return {
        "draft_report": draft,
        "insights": insights,
        "status": "synthesized",
    }
