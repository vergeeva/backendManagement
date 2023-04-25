import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models, Schemas
from app.oauth2 import require_user

router = APIRouter()

@router.get("/DailyPlanner/entry_data", response_model=Schemas.EntryDailyPlannerData)
def get_data_circle(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    entries = db.query(Models.EntryDailyPlanner).filter(Models.EntryDailyPlanner.userId == user_id).all()
    return {'entries': entries}


@router.post("/insert_entry", status_code=status.HTTP_201_CREATED, response_model=Schemas.EntryDailyPlannerBaseSchema)
def insert_value(entries: Schemas.CreateEntrySchema, db: Session = Depends(get_db),
                 owner_id: str = Depends(require_user)):
    entries.userId = uuid.UUID(owner_id)
    new_item = Models.EntryDailyPlanner(**entries.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=Schemas.EntryDailyPlannerBaseSchema)
def update_value(id: str, entry: Schemas.UpdateEntrySchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    entry_query = db.query(Models.EntryDailyPlanner).filter(Models.EntryDailyPlanner.idEntry == id)
    updated_stat = entry_query.first()

    if not updated_stat:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No entry with this id: {id} found')
    if updated_stat.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    entry.userId = user_id
    entry_query.update(stat.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_stat