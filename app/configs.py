from functools import cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.vos import SupportedDataSets


class Configs(BaseSettings):
    """The application configuration."""

    LOG_LEVEL: str = "INFO"

    DATA_SET: SupportedDataSets = SupportedDataSets.KARATE
    SEABORD_STYLE: str = "darkgrid"
    ANALYSIS_N_DECIMAL_PLACES: int = 4

    model_config = SettingsConfigDict(
        env_file=Path("..") / ".env",
        env_file_encoding="utf-8",
    )


@cache
def get_configs() -> Configs:
    return Configs()
