from datetime import date, time
from pydantic import BaseModel, Field, ConfigDict


class LogEntryBase(BaseModel):
    day: date

    start_time: time
    start_place: str = Field(min_length=1, max_length=120)

    end_time: time
    end_place: str = Field(min_length=1, max_length=120)

    km: int | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=500)


class LogEntryCreate(LogEntryBase):
    pass


class LogEntryUpdate(BaseModel):
    # partial update: все поля опциональные
    day: date | None = None

    start_time: time | None = None
    start_place: str | None = Field(default=None, min_length=1, max_length=120)

    end_time: time | None = None
    end_place: str | None = Field(default=None, min_length=1, max_length=120)

    km: int | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=500)


class LogEntryRead(LogEntryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int