import json
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import ResearchState
from models.llm import get_llm_router


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "critic.md"


async def critic_node(state: ResearchState) -> dict:
    """审查草稿报告质量，决定是否需要补充检索"""
    router = get_llm_router()
    llm = router.get_llm("critic")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    human_message = f"""## 研究议题
{state['user_query']}

## 草稿报告
{state['draft_report']}

请审查以上报告，输出审查结果。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_message),
    ]

    response = await llm.ainvoke(messages)
    content = response.content

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        parsed = json.loads(content.strip())
    except (json.JSONDecodeError, IndexError):
        parsed = {
            "needs_revision": False,
            "critique": "JSON 解析失败，默认通过",
            "revision_queries": [],
        }

    return {
        "critique": parsed.get("critique", ""),
        "needs_revision": parsed.get("needs_revision", False),
        "revision_queries": parsed.get("revision_queries", []),
        "status": "criticized",
    }
