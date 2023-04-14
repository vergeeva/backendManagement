from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models, Schemas, oauth2

router = APIRouter()


@router.get('/me', response_model=Schemas.UserBaseSchema)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(Models.User).filter(Models.User.id == user_id).first()
    return user
