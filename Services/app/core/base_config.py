from pydantic_settings import BaseSettings, SettingsConfigDict


from pathlib import Path


class BaseConfig(BaseSettings):
    """BaseConfig class."""
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / "config" / ".env",
        env_file_encoding="utf-8",
    )
