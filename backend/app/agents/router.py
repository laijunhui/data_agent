from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from app.config import settings
from typing import Literal


class LLMRouter:
    def __init__(
        self,
        provider: Literal["openai", "anthropic", "minimax"] = None,
        model: str = None
    ):
        self.provider = provider or settings.default_llm_provider
        self.model = model or settings.default_model

    def get_llm(self) -> BaseChatModel:
        if self.provider == "openai":
            return ChatOpenAI(
                model=self.model,
                api_key=settings.openai_api_key,
                temperature=0
            )
        elif self.provider == "anthropic":
            return ChatAnthropic(
                model=self.model,
                anthropic_api_key=settings.anthropic_api_key,
                temperature=0
            )
        elif self.provider == "minimax":
            return ChatOpenAI(
                model=self.model,
                api_key=settings.minimax_api_key,
                base_url="https://api.minimax.chat/v1",
                temperature=0
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")


def get_llm(provider: str = None, model: str = None) -> BaseChatModel:
    router = LLMRouter(provider, model)
    return router.get_llm()