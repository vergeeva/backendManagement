import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import kanbanSchemas
from app.oauth2 import require_user

router = APIRouter()

@router.get("/circle_kanban_card", response_model=kanbanSchemas.KanbanCardsDataSchema)
def get_kanban_card(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    cards = db.query(Models.KanbanCards).filter(Models.KanbanCards.userId == user_id).all()
    return {'kanbans': cards}


@router.post("/insert_kanban_card", status_code=status.HTTP_201_CREATED,
             response_model=kanbanSchemas.KanbanCardResponse)
def insert_kanban_card(kanbans: kanbanSchemas.CreateKanbanCardSchema, db: Session = Depends(get_db),
                 owner_id: str = Depends(require_user)):
    kanbans.userId = uuid.UUID(owner_id)
    new_item = Models.KanbanCards(**kanbans.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=kanbanSchemas.KanbanCardResponse)
def update_kanban_card(id: str, kanban: kanbanSchemas.UpdateKanbanCardSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    # Запрос в базу данных и получении искомой записи
    kanban_query = db.query(Models.KanbanCards).filter(Models.KanbanCards.idCard == id)
    updated_kanban = kanban_query.first()

    if not updated_kanban:  # Если запись не обнаружена
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'Нет записи с данным кодом: {id}')
    if updated_kanban.userId != uuid.UUID(user_id):  # если коды пользователей не совпали
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Вам запрещено выполнять это действие')
    # передаем код в обновляемый объект
    kanban.userId = user_id
    # создаем запрос на обновление данных
    kanban_query.update(kanban.dict(exclude_unset=True), synchronize_session=False)
    db.commit()  # отправляем изменения
    return updated_kanban  # возвращаем измененный объект


@router.delete('/{id}')
def delete_kanban_card(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    kanban_query = db.query(Models.KanbanCards).filter(Models.KanbanCards.idCard == id)
    kanban = kanban_query.first()
    if not kanban:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No kanban card with this id: {id} found')
    if kanban.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    kanban_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)