"""Application data transfer objects."""

from typing import Any

from pydantic import BaseModel, model_validator

from app.configs import get_configs


class CustomBaseModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def round_floats(cls, data: dict[str, Any]) -> dict[str, Any]:
        configs = get_configs()

        for field, value in data.items():
            if isinstance(value, float):
                data[field] = round(value, configs.ANALYSIS_N_DECIMAL_PLACES)
        return data
