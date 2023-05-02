import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import ganttSchemas
from app.oauth2 import require_user

router = APIRouter()


# Получить все длительности конкретной задачи
@router.get("/gantt_durations_data/{id}", response_model=ganttSchemas.GanttChartTaskDurationList)
def get_gantt_durations_data(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    GanttTasksDuration = db.query(Models.GanttChartTaskDuration).filter(
        Models.GanttChartTaskDuration.ganttTaskId == id).all()
    return {'durations': GanttTasksDuration}


# Добавить длительность конкретной задачи
@router.post("/insert_duration/{id}", status_code=status.HTTP_201_CREATED,
             response_model=ganttSchemas.GanttChartTaskDurationResponse)
def insert_duration(id: str, durations: ganttSchemas.CreateGanttChartTaskDurationSchema, db: Session = Depends(get_db),
                    owner_id: str = Depends(require_user)):
    durations.ganttTaskId = id
    new_item = Models.GanttChartTaskDuration(**durations.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# Обновить длительность
@router.put('/{id}', response_model=ganttSchemas.GanttChartTaskDurationResponse)
def update_duration(id: str, duration: ganttSchemas.UpdateGanttChartTaskDurationSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(require_user)):
    duration_query = db.query(Models.GanttChartTaskDuration).filter(Models.GanttChartTaskDuration.idGanttDuration == id)
    updated_duration = duration_query.first()

    if not updated_duration:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No duration with this id: {id} found')
    duration_query.update(duration.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_duration


# Удалить длительность у задачи
@router.delete('/{id}')
def delete_duration(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    duration_query = db.query(Models.GanttChartTaskDuration).filter(Models.GanttChartTaskDuration.idGanttDuration == id)
    duration = duration_query.first()
    if not duration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No duration with this id: {id} found')
    duration_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
