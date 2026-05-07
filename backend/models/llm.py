from langchain_core.language_models import BaseChatModel
from config import get_settings


class LLMRouter:
    """根据 Agent 角色路由到不同 LLM"""

    def __init__(self):
        self.settings = get_settings()

    def get_llm(self, agent_role: str) -> BaseChatModel:
        # 优先使用 MIMO（统一模型）
        if self.settings.mimo_api_key:
            return self._get_mimo(max_tokens=4096 if agent_role == "synthesizer" else 2048)
        # 回退到 DeepSeek / Claude
        if agent_role == "synthesizer":
            return self._get_claude()
        return self._get_deepseek()

    def _get_mimo(self, max_tokens: int = 2048) -> BaseChatModel:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=self.settings.mimo_model,
            api_key=self.settings.mimo_api_key,
            base_url=self.settings.mimo_base_url,
            max_tokens=max_tokens,
            temperature=0.3,
        )

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


# 全局单例
_router: LLMRouter | None = None


def get_llm_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
