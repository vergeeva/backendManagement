from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


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
