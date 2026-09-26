"""
WHY:
The Config class centralizes application configuration for the ContactBook API.
Using Pydantic Settings ensures that environment variables and .env files are
loaded in a structured, validated way. This keeps configuration separate from
business logic and makes the application easier to deploy across different
environments.

DESIGN:
1. Inherit from BaseSettings to automatically load values from environment
   variables and .env files.
2. Use SettingsConfigDict for Pydantic v2‑compatible configuration such as
   env_file, encoding, and case sensitivity.
3. Provide sensible defaults so the ContactBook API runs even without a .env file.
4. Instantiate a single Config() object so configuration is loaded once and
   shared across the entire application.
"""

from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    app_name: str = "ContactBook API"
    debug: bool = False
    database_url: str = "sqlite:///./contacts.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


config = Config()
