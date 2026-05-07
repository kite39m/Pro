from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import ResearchState
from models.llm import get_llm_router
from utils.markdown import format_sources_section


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "writer.md"


async def writer_node(state: ResearchState) -> dict:
    """将草稿润色为最终研报"""
    router = get_llm_router()
    llm = router.get_llm("writer")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    sources_section = format_sources_section(state["sources"])

    human_message = f"""## 研究议题
{state['user_query']}

## 草稿报告
{state['draft_report']}

## 审查意见
{state['critique']}

## 数据来源
{sources_section}

请将草稿润色为最终研报格式。保留所有数据引用，补充来源附录。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_message),
    ]

    response = await llm.ainvoke(messages)

    return {
        "final_report": response.content,
        "status": "completed",
    }
