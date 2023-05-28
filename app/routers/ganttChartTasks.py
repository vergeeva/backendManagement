import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import ganttSchemas
from app.oauth2 import require_user

router = APIRouter()


# получить список задач
@router.get("/gantt_tasks_data", response_model=ganttSchemas.GanttChartTasksData)
def get_gantt_tasks_data(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    GanttTasks = db.query(Models.GanttChartTasks).filter(Models.GanttChartTasks.userId == user_id).all()
    return {'GanttTasks': GanttTasks}


# Добавить задачу
@router.post("/insert_gantt_task", status_code=status.HTTP_201_CREATED,
             response_model=ganttSchemas.GanttChartTasksResponse)
def insert_gantt_task(tasks: ganttSchemas.CreateGanttChartTasksSchema, db: Session = Depends(get_db),
                      owner_id: str = Depends(require_user)):
    tasks.userId = uuid.UUID(owner_id)
    new_item = Models.GanttChartTasks(**tasks.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# Обновить задачу
@router.put('/{id}', response_model=ganttSchemas.GanttChartTasksResponse)
def update_gantt_task(id: str, task: ganttSchemas.UpdateGanttChartTasksSchema, db: Session = Depends(get_db),
                      user_id: str = Depends(require_user)):
    tasks_query = db.query(Models.GanttChartTasks).filter(Models.GanttChartTasks.idGanttTask == id)
    updated_task = tasks_query.first()

    if not updated_task:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No task with this id: {id} found')
    if updated_task.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    task.userId = user_id
    tasks_query.update(task.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_task


# Удалить задачу
@router.delete('/{id}')
def delete_gantt_task(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    task_query = db.query(Models.GanttChartTasks).filter(Models.GanttChartTasks.idGanttTask == id)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No task with this id: {id} found')
    if task.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
