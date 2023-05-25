import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import kanbanSchemas
from app.oauth2 import require_user

router = APIRouter()


# Получить список задач в карточке
@router.get("/tasks_in_card/{id}", response_model=kanbanSchemas.TaskInCardData)
def get_tasks_in_card(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    tasks = db.query(Models.TaskInCards).filter(Models.TaskInCards.cardId == id).all()
    return {'tasks': tasks}

# Добавить задачу в карточку
@router.post("/insert_task/{id}", status_code=status.HTTP_201_CREATED,
             response_model=kanbanSchemas.TasksInCardResponse)
def insert_task(id: str, tasks: kanbanSchemas.CreateTaskInCardSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    tasks.kanbanCardId = uuid.UUID(id)
    new_item = Models.TaskInCards(**tasks.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# Обновить задачу из карточки
@router.put('/{id}', response_model=kanbanSchemas.TasksInCardResponse)
def update_value(id: str, task: kanbanSchemas.UpdateTaskInCardSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    task_query = db.query(Models.TaskInCards).filter(Models.TaskInCards.id == id)
    updated_task = task_query.first()

    if not updated_task:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'Нет задачи с заданным кодом: {id}')
    task_query.update(task.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_task


# Удалить задачку в карточке
@router.delete('/{id}')
def delete_value(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    task_query = db.query(Models.TaskInCards).filter(Models.TaskInCards.id == id)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No stat with this id: {id} found')
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
