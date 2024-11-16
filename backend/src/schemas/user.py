from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class CustomBaseModel(BaseModel):
    id: str = Field(validation_alias='_id')

    @field_validator("id", mode="before")
    def convert_object_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class UserOutDTO(CustomBaseModel):
    username: str
    hashed_password: str

    model_config = {
        'extra': 'allow'
    }