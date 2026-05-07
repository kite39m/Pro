# osint-engine/backend/config.py
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

# .env 文件在项目根目录 (osint-engine/.env)
ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    # LLM
    deepseek_api_key: str = ""
    anthropic_api_key: str = ""
    qwen_api_key: str = ""
    mimo_api_key: str = ""
    mimo_base_url: str = "https://api.xiaomimimo.com/v1"
    mimo_model: str = "mimo-v2.5-pro"

    # Search
    serpapi_api_key: str = ""

    # Database
    database_url: str = "sqlite:///data/osint.db"

    # Server
    backend_port: int = 8000
    frontend_port: int = 3000

    # Agent timeouts (seconds)
    planner_timeout: int = 60
    researcher_timeout: int = 120
    synthesizer_timeout: int = 120
    critic_timeout: int = 60
    writer_timeout: int = 60

    # Crawler
    crawler_timeout: int = 10
    crawler_max_content_bytes: int = 50000

    model_config = {"env_file": str(ENV_FILE), "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
