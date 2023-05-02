from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr, validator


# Задачи в диаграмме Гантта
class GanttChartTasksSchema(BaseModel):
    nameOfTask: str

    class Config:
        orm_mode = True


class GanttChartTasksResponse(GanttChartTasksSchema):
    idGanttTask: uuid.UUID


class CreateGanttChartTasksSchema(GanttChartTasksSchema):
    userId: uuid.UUID | None = None


class UpdateGanttChartTasksSchema(BaseModel):
    nameOfTask: str
    userId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class GanttChartTasksData(BaseModel):
    GanttTasks: List[GanttChartTasksResponse]


# ----------------------------------------------------------------------------------------------------------------------
# Схемы для длительности задач в диаграмме Гантта

class GanttChartTaskDurationBaseSchema(BaseModel):
    ganttTaskStart: datetime
    ganttTaskEnd: datetime

    class Config:
        orm_mode = True

    @validator('ganttTaskStart', 'ganttTaskEnd', pre=True, always=True)
    def convert_date(cls, value):
        return value


class GanttChartTaskDurationResponse(GanttChartTaskDurationBaseSchema):
    idGanttDuration: uuid.UUID


class CreateGanttChartTaskDurationSchema(GanttChartTaskDurationBaseSchema):
    ganttTaskId: uuid.UUID | None = None  # код задачи, чья длительность


class UpdateGanttChartTaskDurationSchema(BaseModel):
    ganttTaskStart: datetime
    ganttTaskId: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class GanttChartTaskDurationList(BaseModel):
    durations: List[GanttChartTaskDurationResponse]
