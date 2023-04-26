from datetime import datetime, timedelta, date
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для записей в ежедневник
class EntryDailyPlannerBaseSchema(BaseModel):
    dailyTaskName: str
    taskStart: datetime
    taskEnd: datetime
    taskColor: str
    taskStatus: bool = False

    class Config:
        orm_mode = True


class EntryDailyPlannerResponse(EntryDailyPlannerBaseSchema):
    idEntry: uuid.UUID


class CreateEntrySchema(EntryDailyPlannerBaseSchema):
    userId: uuid.UUID | None = None


class UpdateEntrySchema(BaseModel):
    idTaskInCard: uuid.UUID
    dailyTaskName: str
    taskStart: datetime
    taskEnd: datetime
    taskColor: str
    taskStatus: bool
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EntryDailyPlannerData(BaseModel):
    entries: List[EntryDailyPlannerResponse]