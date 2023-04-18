from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для пользователя
class UserBaseSchema(BaseModel):
    firstName: str
    lastName: str
    patronymic: str
    email: EmailStr

    class Config:
        orm_mode = True


class LoginUserSchema(BaseModel):
    login: str
    password: constr(min_length=8)


class CreateUserSchema(UserBaseSchema):
    login: str
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


# Схемы для колеса баланса
class CircleValueBaseSchema(BaseModel):
    label: str
    value: int


class BalanceCircleData(BaseModel):
    stats: List[CircleValueBaseSchema]


class CreateValueSchema(CircleValueBaseSchema):
    user_id: uuid.UUID | None = None


class UpdateValueSchema(BaseModel):
    label: str
    value: int
    user_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
