from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models, Schemas, oauth2, utils
from app.oauth2 import require_user
import uuid

router = APIRouter()


@router.get('/me', response_model=Schemas.UserBaseSchema)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(Models.User).filter(Models.User.id == user_id).first()
    return user


@router.put('/update_profile', response_model=Schemas.UserBaseSchema)
def update_profile(user: Schemas.UpdateUserSchema, db: Session = Depends(get_db),
                   user_id: str = Depends(require_user)):
    user_query = db.query(Models.User).filter(Models.User.id == user_id)
    updated_user = user_query.first()

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No user with this id: {id} found')
    if updated_user.id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    user.password = utils.hash_password(user.password)
    user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_user
