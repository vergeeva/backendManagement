import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import listSchemas
from app.oauth2 import require_user

router = APIRouter()


# Получить все задачи из списка
@router.get("/tasks_in_list", response_model=listSchemas.ItemListData)
def get_tasks_in_list(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    items = db.query(Models.ItemsList).filter(Models.ItemsList.userId == user_id).all()
    return {'items': items}


# Добавить задачу в список
@router.post("/insert_task_in_list", status_code=status.HTTP_201_CREATED,
             response_model=listSchemas.ItemListResponse)
def insert_task_in_list(item: listSchemas.CreateItemListSchema, db: Session = Depends(get_db),
                        user_id: str = Depends(require_user)):
    item.userId = uuid.UUID(user_id)
    new_item = Models.ItemsList(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# обновить конкретную задачу
@router.put('/{id}', response_model=listSchemas.ItemListResponse)
def update_item(id: str, item: listSchemas.UpdateItemListSchema, db: Session = Depends(get_db),
                user_id: str = Depends(require_user)):
    item_query = db.query(Models.ItemsList).filter(Models.ItemsList.idTaskInList == id)
    updated_item = item_query.first()

    if not updated_item:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No item with this id: {id} found')

    item_query.update(item.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_item


# Удалить конкретную задачу
@router.delete('/{id}')
def delete_item(id: str, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    item_query = db.query(Models.ItemsList).filter(Models.ItemsList.idTaskInList == id)
    item = item_query.first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No stat with this id: {id} found')
    item_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
