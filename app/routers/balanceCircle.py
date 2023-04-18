import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models, Schemas
from app.oauth2 import require_user

router = APIRouter()


@router.get("/circle_data", response_model=Schemas.BalanceCircleData)
def get_data_circle(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    stats = db.query(Models.BalanceCircle).filter(Models.BalanceCircle.userId == user_id)
    return stats


@router.post("/insert_value", status_code=status.HTTP_201_CREATED, response_model=Schemas.CircleValueBaseSchema)
def insert_value(stats: Schemas.CreateValueSchema, db: Session = Depends(get_db),
                 owner_id: str = Depends(require_user)):
    stats.user_id = uuid.UUID(owner_id)
    new_item = Models.BalanceCircle(**stats.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=Schemas.CircleValueBaseSchema)
def update_value(id: str, stat: Schemas.UpdateValueSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    stat_query = db.query(Models.BalanceCircle).filter(Models.BalanceCircle.idBalance == id)
    updated_stat = stat_query.first()

    if not updated_stat:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No stat with this id: {id} found')
    if updated_stat.user_id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    stat.user_id = user_id
    stat_query.update(stat.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_stat


@router.delete('/{id}')
def delete_value(id: str,db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    stat_query=db.query(Models.BalanceCircle).filter(Models.BalanceCircle.idBalance == id)
    stat = stat_query.first()
    if not stat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No stat with this id: {id} found')
    if stat.user_id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    stat_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)