from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


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
