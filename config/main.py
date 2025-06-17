from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / "settings" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )



class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="TG_"
    )
    bot_token: str
    chat_id: str
    chat_link: str
    admins: List[int]

class DataBaseConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="DB_"
    )
    host_url: str

class LoggerConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="LOG_"
    )
    logger: str


class AppConfig(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    db: DataBaseConfig = Field(default_factory=DataBaseConfig)
    logger: LoggerConfig = Field(default_factory=LoggerConfig)

    @classmethod
    def load(cls) -> "AppConfig":
        return cls()


config = AppConfig.load()