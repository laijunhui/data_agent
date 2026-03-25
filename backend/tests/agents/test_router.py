import pytest
from app.agents.router import LLMRouter, get_llm


def test_llm_router_openai():
    router = LLMRouter(provider="openai", model="gpt-4")
    llm = router.get_llm()
    assert llm is not None


def test_llm_router_anthropic():
    router = LLMRouter(provider="anthropic", model="claude-3-opus")
    llm = router.get_llm()
    assert llm is not None


def test_get_llm_default():
    llm = get_llm()
    assert llm is not None