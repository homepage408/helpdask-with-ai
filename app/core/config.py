from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = Field(default="HelpDesk Mini")
    ENVIRONMENT: Literal["development", "staging", "production", "test"] = Field(
        default="development"
    )
    DEBUG: bool = Field(default=True)
    API_V1_PREFIX: str = Field(default="/api/v1")

    # Database Settings
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/helpdesk_mini"
    )
    TEST_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/helpdesk_mini_test"
    )
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    DB_POOL_PRE_PING: bool = Field(default=True)

    # Security & JWT
    JWT_SECRET_KEY: str = Field(
        default="insecure-dev-secret-key-change-in-production-min-32-chars-long!"
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # CORS
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
