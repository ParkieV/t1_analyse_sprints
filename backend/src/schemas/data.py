import math
from datetime import datetime
from typing import Optional

from pydantic import field_validator, model_validator

from src.schemas.user import CustomBaseModel


class HistoriesOutDTO(CustomBaseModel):
    entity_id: int | None
    history_property_name: str | None
    history_date: datetime | None
    history_version: int | None
    history_change_type: str | None
    history_change: str | None

    @field_validator("history_date", mode="before")
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%m/%d/%y %H:%M")

    @model_validator(mode="before")
    def handle_nan(cls, values):
        return {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in values.items()}

class EntitiesOutDTO(CustomBaseModel):
    entity_id: int | None
    area: str | None
    type: str | None
    status: str | None
    state: str | None
    priority: str | None
    ticket_number: str | None
    name: str | None
    create_date: datetime | None
    created_by: str | None
    update_date: datetime | None
    updated_by: str | None
    parent_ticket_id: int | None
    assignee: str | None
    owner: str | None
    due_date: datetime | None
    rank: str | None
    estimation: float | None
    spent: int | None
    workgroup: str | None
    resolution: str | None

    @field_validator("due_date", mode="before")
    def convert_datetime(cls, value):
        if (value is None) or isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%m/%d/%y")

    @model_validator(mode="before")
    def handle_nan(cls, values):
        return {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in values.items()}

class EntityOutDTO(EntitiesOutDTO):
    history_ids: list[HistoriesOutDTO]

class SprintBaseDTO(CustomBaseModel):
    sprint_name: str | None
    sprint_status: str | None
    sprint_start_date: datetime | None
    sprint_end_date: datetime | None
    progress: float | None

class SprintsOutDTO(SprintBaseDTO):
    update_date: datetime | None

class SprintOutDTO(SprintBaseDTO):
    entities: list[EntitiesOutDTO] | None
