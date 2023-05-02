import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import kanbanSchemas
from app.oauth2 import require_user

router = APIRouter()


@router.get("/types_data", response_model=kanbanSchemas.TypeCardsKanbanData)
def get_types_data(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    types = db.query(Models.TypeOfCards).all()
    return {'types': types}


@router.post("/insert_type", status_code=status.HTTP_201_CREATED,
             response_model=kanbanSchemas.TypeCardsKanbanResponse)
def insert_type(types: kanbanSchemas.CreateTypeCardsKanban, db: Session = Depends(get_db),
                 owner_id: str = Depends(require_user)):
    new_item = Models.TypeOfCards(**types.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=kanbanSchemas.TypeCardsKanbanResponse)
def update_type(id: str, type: kanbanSchemas.UpdateTypeCardsKanban, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    type_query = db.query(Models.TypeOfCards).filter(Models.TypeOfCards.idType == id)
    updated_type = type_query.first()

    if not updated_type:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No type with this id: {id} found')
    type_query.update(type.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_type


@router.delete('/{id}')
def delete_type(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    type_query = db.query(Models.TypeOfCards).filter(Models.TypeOfCards.idType == id)
    type = type_query.first()
    if not type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No stat with this id: {id} found')
    type_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)