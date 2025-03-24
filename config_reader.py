from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str  # Changed from SecretStr
    supabase_url: str  # Changed from SecretStr
    supabase_key: str  # Changed from SecretStr

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


config = Settings()
