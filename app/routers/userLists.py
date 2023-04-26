import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import listSchemas
from app.oauth2 import require_user

router = APIRouter()


# Получить все списки, которые создал пользователь
@router.get("/lists_data", response_model=listSchemas.UserListData)
def get_lists_data(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    lists = db.query(Models.UserLists).filter(Models.UserLists.userId == user_id).all()
    return {'stats': lists}


# Добавить новый список
@router.post("/insert_list", status_code=status.HTTP_201_CREATED,
             response_model=listSchemas.UserListResponse)
def insert_list(list: listSchemas.CreateUserListSchema, db: Session = Depends(get_db),
                 owner_id: str = Depends(require_user)):
    list.userId = uuid.UUID(owner_id)
    new_item = Models.UserLists(**list.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=listSchemas.UserListResponse)
def update_list(id: str, list: listSchemas.UpdateUserListSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    list_query = db.query(Models.UserLists).filter(Models.UserLists.idUserList == id)
    updated_list = list_query.first()

    if not updated_list:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No list with this id: {id} found')
    if updated_list.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    list.userId = user_id
    list_query.update(list.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_list


@router.delete('/{id}')
def delete_list(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    list_query = db.query(Models.UserLists).filter(Models.UserLists.idUserList == id)
    list = list_query.first()
    if not list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No list with this id: {id} found')
    if list.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    list_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
