# osint-engine/backend/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM
    deepseek_api_key: str = ""
    anthropic_api_key: str = ""
    qwen_api_key: str = ""

    # Search
    serpapi_api_key: str = ""

    # Database
    database_url: str = "sqlite:///data/osint.db"

    # Server
    backend_port: int = 8000

    # Agent timeouts (seconds)
    planner_timeout: int = 60
    researcher_timeout: int = 120
    synthesizer_timeout: int = 120
    critic_timeout: int = 60
    writer_timeout: int = 60

    # Crawler
    crawler_timeout: int = 10
    crawler_max_content_bytes: int = 50000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
