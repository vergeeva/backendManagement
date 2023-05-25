from datetime import datetime, timedelta, date
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr, root_validator, validator


# Схемы для записей в ежедневник
class EntryDailyPlannerBaseSchema(BaseModel):
    dailyTaskName: str
    taskStart: datetime
    taskEnd: datetime
    taskColor: str

    class Config:
        orm_mode = True

    @validator('taskStart', 'taskEnd', pre=True, always=True)
    def convert_date(cls, value):
        return value


class EntryDailyPlannerResponse(EntryDailyPlannerBaseSchema):
    idEntry: uuid.UUID


class CreateEntrySchema(EntryDailyPlannerBaseSchema):
    userId: uuid.UUID | None = None


class UpdateEntrySchema(BaseModel):
    dailyTaskName: str
    taskStart: datetime
    taskEnd: datetime
    taskColor: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator('taskStart', 'taskEnd', pre=True, always=True)
    def convert_date(cls, value):
        return value


class EntryDailyPlannerData(BaseModel):
    entries: List[EntryDailyPlannerResponse]
