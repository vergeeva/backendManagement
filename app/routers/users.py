from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models, oauth2, utils
from ..Schemas import userSchemas
from app.oauth2 import require_user
import uuid

router = APIRouter()


@router.get('/me', response_model=userSchemas.UserResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(Models.User).filter(Models.User.id == user_id).first()
    return user


@router.put('/update_profile', response_model=userSchemas.UserResponse)
def update_profile(user: userSchemas.UpdateUserSchema, db: Session = Depends(get_db),
                   user_id: str = Depends(require_user)):
    user_query = db.query(Models.User).filter(Models.User.id == user_id)
    updated_user = user_query.first()

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'Не существует пользователя с этим кодом: {id}')
    if updated_user.id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='У вас нет разрешения на данное действие')
    # user.password = utils.hash_password(user.password)
    user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_user


@router.put('/update_user_password', response_model=userSchemas.UserResponse)
def update_user_password(user: userSchemas.UserUpdatePassword, db: Session = Depends(get_db),
                   user_id: str = Depends(require_user)):
    user_query = db.query(Models.User).filter(Models.User.id == user_id)
    updated_user = user_query.first()

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'Не существует пользователя с этим кодом: {id}')
    if updated_user.id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='У вас нет разрешения на данное действие')
    user.password = utils.hash_password(user.password)
    user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_user
