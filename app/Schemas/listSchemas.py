from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для списков
class UserListBaseSchema(BaseModel):
    nameOfList: str

    class Config:
        orm_mode = True


class UserListResponse(UserListBaseSchema):
    idUserList: uuid.UUID


class CreateUserListSchema(UserListBaseSchema):
    userId: uuid.UUID


class UpdateUserListSchema(BaseModel):
    idUserList: uuid.UUID
    nameOfList: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserListData(BaseModel):
    lists: List[UserListResponse]


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для данных в списке
class ItemListBaseSchema(BaseModel):
    textOfItem: str
    isChecked: bool = False

    class Config:
        orm_mode = True


class ItemListResponse(ItemListBaseSchema):
    idTaskInList: uuid.UUID


class CreateItemListSchema(ItemListBaseSchema):
    userListsId: uuid.UUID  # Код списка, в котором хранится задача


class UpdateItemListSchema(BaseModel):
    idTaskInList: uuid.UUID
    textOfItem: str
    isChecked: bool
    userListsId: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ItemListData(BaseModel):
    items: List[ItemListResponse]

