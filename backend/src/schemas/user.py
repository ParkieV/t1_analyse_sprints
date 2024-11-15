from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field, validator, field_validator


class UserDBOutDTO(BaseModel):
    id: str = Field(validation_alias='_id',)
    username: str
    hashed_password: str

    @field_validator("id", mode="before")
    def convert_object_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    model_config = {
        'extra': 'allow'
    }