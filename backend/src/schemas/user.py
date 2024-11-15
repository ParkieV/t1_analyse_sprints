from typing import Any

from pydantic import BaseModel, Field


class UserDBOutDTO(BaseModel):
    id: Any = Field(validation_alias='_id')
    username: str
    hashed_password: str

    model_config = {
        'extra': 'allow'
    }