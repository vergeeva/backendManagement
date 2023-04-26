import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import technicSchemas
from app.oauth2 import require_user

router = APIRouter()


@router.get("/technics_data", response_model=technicSchemas.TechnicListSchema)
def get_technics_data(db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    technics = db.query(Models.TechnicsSettings).filter(Models.TechnicsSettings.userId == user_id).all()
    return {'technics': technics}


@router.post("/insert_technic", status_code=status.HTTP_201_CREATED, response_model=technicSchemas.TechnicResponse)
def insert_technic_settings(technics: technicSchemas.CreateTechnicSchema, db: Session = Depends(get_db),
                            user_id: str = Depends(require_user)):
    technics.userId = uuid.UUID(user_id)
    new_item = Models.TechnicsSettings(**technics.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=technicSchemas.TechnicResponse)
def update_technic_settings(id: str, technic: technicSchemas.UpdateTechnicSchema, db: Session = Depends(get_db),
                 user_id: str = Depends(require_user)):
    technic_query = db.query(Models.TechnicsSettings).filter(Models.TechnicsSettings.idTechnic == id)
    updated_technic = technic_query.first()

    if not updated_technic:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No technic with this id: {id} found')
    if updated_technic.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    technic.userId = user_id
    technic_query.update(technic.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_technic


@router.delete('/{id}')
def delete_technic_settings(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    technic_query=db.query(Models.TechnicsSettings).filter(Models.TechnicsSettings.idTechnic == id)
    technic = technic_query.first()
    if not technic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No technic with this id: {id} found')
    if technic.userId != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    technic_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

