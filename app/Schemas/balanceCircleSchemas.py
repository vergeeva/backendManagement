from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для колеса баланса
class CircleValueBaseSchema(BaseModel):
    labelItem: str
    value: int

    class Config:
        orm_mode = True


class BalanceCircleResponse(CircleValueBaseSchema):
    idBalance: uuid.UUID


class BalanceCircleData(BaseModel):
    stats: List[BalanceCircleResponse]


class CreateValueSchema(CircleValueBaseSchema):
    userId: uuid.UUID | None = None


class UpdateValueSchema(BaseModel):
    labelItem: str
    value: int
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
