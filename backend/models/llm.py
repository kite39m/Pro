# osint-engine/backend/models/llm.py
from langchain_core.language_models import BaseChatModel
from config import get_settings


class LLMRouter:
    """根据 Agent 角色路由到不同 LLM"""

    def __init__(self):
        self.settings = get_settings()

    def get_llm(self, agent_role: str) -> BaseChatModel:
        if agent_role == "synthesizer":
            return self._get_claude()
        return self._get_deepseek()

    def _get_deepseek(self) -> BaseChatModel:
        from langchain_deepseek import ChatDeepSeek
        return ChatDeepSeek(
            model="deepseek-chat",
            api_key=self.settings.deepseek_api_key,
            max_tokens=2048,
            temperature=0.3,
        )

    def _get_claude(self) -> BaseChatModel:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-sonnet-4-6",
            api_key=self.settings.anthropic_api_key,
            max_tokens=4096,
            temperature=0.3,
        )

    def get_llm_with_fallback(self, agent_role: str) -> BaseChatModel:
        """获取 LLM，主模型失败时自动 fallback"""
        try:
            return self.get_llm(agent_role)
        except Exception:
            return self._get_claude() if agent_role != "synthesizer" else self._get_deepseek()


# 全局单例
_router: LLMRouter | None = None


def get_llm_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
