from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для техник
class TechnicBaseSchema(BaseModel):
    settingsName: str
    workTimer: int
    shortBreak: int
    longBreak: int
    countOfCycles: int

    class Config:
        orm_mode = True


class TechnicResponse(TechnicBaseSchema):
    idTechnic: uuid.UUID


class CreateTechnicSchema(TechnicBaseSchema):
    userId: uuid.UUID | None = None


class TechnicListSchema(BaseModel):
    technics: List[TechnicResponse]


class UpdateTechnicSchema(BaseModel):
    settingsName: str
    workTimer: int
    shortBreak: int
    longBreak: int
    countOfCycles: int
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
