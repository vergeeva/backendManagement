from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


# Схемы для карточек канбан
class KanbanCardBaseSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class CreateKanbanCardSchema(KanbanCardBaseSchema):
    userId: uuid.UUID | None = None


class UpdateKanbanCardSchema(BaseModel):
    title: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None





# ----------------------------------------------------------------------------------------------------------------------
# Для типов карточек канбан
# class TypeCardsKanbanBaseSchema(BaseModel):
#     typeName: str
#
#     class Config:
#         orm_mode = True
#
#
# class TypeCardsKanbanResponse(TypeCardsKanbanBaseSchema):
#     idType: uuid.UUID
#
#
# class CreateTypeCardsKanban(TypeCardsKanbanBaseSchema):
#     pass
#
#
# class UpdateTypeCardsKanban(BaseModel):
#     typeName: str
#     created_at: datetime | None = None
#     updated_at: datetime | None = None
#
#
# class TypeCardsKanbanData(BaseModel):
#     types: List[TypeCardsKanbanResponse]
#

# ----------------------------------------------------------------------------------------------------------------------
# Для задач в карточке канбан
class TasksInCardBaseSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class TasksInCardResponse(TasksInCardBaseSchema):
    id: uuid.UUID


class CreateTaskInCardSchema(TasksInCardBaseSchema):
    kanbanCardId: uuid.UUID | None = None


class UpdateTaskInCardSchema(BaseModel):
    title: str
    description: str
    kanbanCardId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskInCardData(BaseModel):
    cards: List[TasksInCardResponse]


class KanbanCardResponse(KanbanCardBaseSchema):
    id: uuid.UUID
    cards: List[TasksInCardResponse] | None = None


class KanbanCardResponseInsert(KanbanCardBaseSchema):
    id: uuid.UUID

class KanbanCardsDataSchema(BaseModel):
    columns: List[KanbanCardResponse]
