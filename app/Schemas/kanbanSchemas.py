from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для карточек канбан
class KanbanCardBaseSchema(BaseModel):
    typeOfCard: uuid.UUID

    class Config:
        orm_mode = True


class KanbanCardResponse(KanbanCardBaseSchema):
    idCard: uuid.UUID


class CreateKanbanCardSchema(KanbanCardBaseSchema):
    userId: uuid.UUID | None = None


class UpdateKanbanCardSchema(BaseModel):
    typeOfCard: uuid.UUID
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class KanbanCardsDataSchema(BaseModel):
    kanbans: List[KanbanCardResponse]


# ----------------------------------------------------------------------------------------------------------------------
# Для типов карточек канбан
class TypeCardsKanbanBaseSchema(BaseModel):
    typeName: str

    class Config:
        orm_mode = True


class TypeCardsKanbanResponse(TypeCardsKanbanBaseSchema):
    idType: uuid.UUID


class CreateTypeCardsKanban(TypeCardsKanbanBaseSchema):
    pass


class UpdateTypeCardsKanban(BaseModel):
    typeName: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TypeCardsKanbanData(BaseModel):
    types: List[TypeCardsKanbanResponse]


# ----------------------------------------------------------------------------------------------------------------------
# Для задач в карточке канбан
class TasksInCardBaseSchema(BaseModel):
    taskText: str
    isDone: bool = False

    class Config:
        orm_mode = True


class TasksInCardResponse(TasksInCardBaseSchema):
    idTaskInCard: uuid.UUID


class CreateTaskInCardSchema(TasksInCardBaseSchema):
    cardId: uuid.UUID | None = None


class UpdateTaskInCardSchema(BaseModel):
    taskText: str
    isDone: bool
    cardId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskInCardData(BaseModel):
    tasks: List[TasksInCardResponse]
