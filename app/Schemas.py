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


class UpdateUserSchema(BaseModel):
    login: str
    password: constr(min_length=8)
    firstName: str
    lastName: str
    patronymic: str
    email: EmailStr
    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


# Схемы для колеса баланса
class CircleValueBaseSchema(BaseModel):
    labelItem: str
    value: int

    class Config:
        orm_mode = True


class BalanceCircleData(BaseModel):
    stats: List[CircleValueBaseSchema]


class CreateValueSchema(CircleValueBaseSchema):
    userId: uuid.UUID | None = None


class UpdateValueSchema(BaseModel):
    labelItem: str
    value: int
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


# Схемы для техник
class TechnicBaseSchema(BaseModel):
    settingsName: str
    workTimer: int
    shortBreak: int
    longBreak: int
    countOfCycles: int

    class Config:
        orm_mode = True


class CreateTechnicSchema(TechnicBaseSchema):
    userId: uuid.UUID | None = None


class TechnicListSchema(BaseModel):
    technics: List[TechnicBaseSchema]


class UpdateTechnicSchema(BaseModel):
    settingsName: str
    workTimer: int
    shortBreak: int
    longBreak: int
    countOfCycles: int
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
