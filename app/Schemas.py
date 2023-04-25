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


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для колеса баланса
class CircleValueBaseSchema(BaseModel):
    idBalance: uuid.UUID
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


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для техник
class TechnicBaseSchema(BaseModel):
    idTechnic: uuid.UUID
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


# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для записей в ежедневник
class EntryDailyPlannerBaseSchema(BaseModel):
    idTaskInCard: uuid.UUID
    dailyTaskName: str
    taskStart: datetime
    taskEnd: datetime
    taskColor: str
    taskStatus: bool = False

    class Config:
        orm_mode = True


class CreateEntrySchema(EntryDailyPlannerBaseSchema):
    userId: uuid.UUID


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
    entries: List[EntryDailyPlannerBaseSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для списка пользователей
class UserListBaseSchema(BaseModel):
    idUserList: uuid.UUID
    nameOfList: str

    class Config:
        orm_mode = True


class CreateUserListSchema(UserListBaseSchema):
    userId: uuid.UUID


class UpdateUserListSchema(BaseModel):
    idUserList: uuid.UUID
    nameOfList: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserListData(BaseModel):
    lists: List[UserListBaseSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для данных в списке
class ItemListBaseSchema(BaseModel):
    idTaskInList: uuid.UUID
    textOfItem: str
    isChecked: bool = False

    class Config:
        orm_mode = True


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
    items: List[ItemListBaseSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Задачи в диаграмме Гантта
class GanttChartTasksSchema(BaseModel):
    idGanttTask: uuid.UUID
    nameOfTask: str

    class Config:
        orm_mode = True


class CreateGanttChartTasksSchema(GanttChartTasksSchema):
    userId: uuid.UUID


class UpdateGanttChartTasksSchema(BaseModel):
    idGanttTask: uuid.UUID
    nameOfTask: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class GanttChartTasksData(BaseModel):
    GanttTasks: List[GanttChartTasksSchema]


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для длительности задач в диаграмме Гантта

class GanttChartTaskDurationBaseSchema(BaseModel):
    idGanttTask: uuid.UUID
    ganttTaskStart: datetime
    ganttTaskEnd: datetime

    class Config:
        orm_mode = True


class CreateGanttChartTaskDurationSchema(GanttChartTaskDurationBaseSchema):
    projectId: uuid.UUID


class UpdateGanttChartTaskDurationSchema(BaseModel):
    idGanttTask: uuid.UUID
    ganttTaskStart: datetime
    ganttTaskEnd: datetime
    projectId: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
