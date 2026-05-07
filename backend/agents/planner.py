import json
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import ResearchState
from models.llm import get_llm_router


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "planner.md"


async def planner_node(state: ResearchState) -> dict:
    """将宏观指令拆解为子检索任务"""
    router = get_llm_router()
    llm = router.get_llm("planner")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请分析以下研究议题并拆解为子任务：\n\n{state['user_query']}"),
    ]

    response = await llm.ainvoke(messages)

    # 解析 JSON 输出
    content = response.content
    try:
        # 提取 JSON 块（兼容 markdown 代码块）
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        parsed = json.loads(content.strip())
        sub_tasks = parsed.get("sub_tasks", [])
    except (json.JSONDecodeError, IndexError):
        # fallback: 单个子任务
        sub_tasks = [{
            "topic": "综合分析",
            "search_keywords_zh": [state["user_query"]],
            "search_keywords_en": [state["user_query"]],
            "priority": "high",
        }]

    return {
        "sub_tasks": sub_tasks,
        "status": "planned",
    }
