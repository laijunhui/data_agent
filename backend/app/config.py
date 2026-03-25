from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str

    # LLM
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    minimax_api_key: str = ""
    minimax_group_id: str = ""
    default_llm_provider: Literal["openai", "anthropic", "minimax"] = "openai"
    default_model: str = "gpt-4-turbo-preview"

    class Config:
        env_file = ".env"


settings = Settings()