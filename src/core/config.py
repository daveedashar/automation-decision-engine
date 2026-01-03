"""Core configuration."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = False
    app_secret_key: str = "change-me"
    
    database_url: str = "postgresql+asyncpg://localhost/decision_db"
    redis_url: str = "redis://localhost:6379/0"
    
    rules_directory: str = "rules/"
    rules_reload_interval: int = 60
    
    decision_log_enabled: bool = True
    decision_log_retention_days: int = 90
    
    ab_testing_enabled: bool = True
    default_traffic_split: int = 50
    
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()
