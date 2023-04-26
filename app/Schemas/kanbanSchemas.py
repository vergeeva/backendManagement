from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для карточек канбан
class KanbanCardBaseSchema(BaseModel):
    idCard: uuid.UUID
    typeOfCard: uuid.UUID

    class Config:
        orm_mode = True


class CreateKanbanCardSchema(KanbanCardBaseSchema):
    userId: uuid.UUID | None = None


class UpdateKanbanCardSchema(BaseModel):
    typeOfCard: uuid.UUID
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class KanbanCardsDataSchema(BaseModel):
    kanbans: List[KanbanCardBaseSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Для типов карточек канбан
class TypeCardsKanbanBaseSchema(BaseModel):
    idType: uuid.UUID
    typeName: str

    class Config:
        orm_mode = True


class CreateTypeCardsKanban(TypeCardsKanbanBaseSchema):
    pass


class UpdateTypeCardsKanban(BaseModel):
    idType: uuid.UUID
    typeName: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TypeCardsKanbanData(BaseModel):
    types: List[TypeCardsKanbanBaseSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Для задач в карточке канбан
class TasksInCardBaseSchema(BaseModel):
    idTaskInCard: uuid.UUID
    taskText: str
    isDone: bool = False

    class Config:
        orm_mode = True


class CreateTaskInCardSchema(TasksInCardBaseSchema):
    cardId: uuid.UUID


class UpdateTaskInCardSchema(BaseModel):
    idTaskInCard: uuid.UUID
    taskText: str
    isDone: bool
    cardId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskInCardData(BaseModel):
    tasks: List[TasksInCardBaseSchema]
