import hashlib
from datetime import timedelta
from random import randbytes

from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from starlette.responses import JSONResponse

from app import oauth2
from .. import Models, utils
from ..Schemas import userSchemas
from sqlalchemy.orm import Session
from ..database import get_db
from app.oauth2 import AuthJWT
from ..config import settings
from app.mail import email
# from ..email import send_email_async


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)  # Регистрация пользователя
async def create_user(payload: userSchemas.CreateUserSchema, request: Request, db: Session = Depends(get_db)):
    user_query = db.query(Models.User).filter(
        Models.User.login == payload.login.lower())  # Ищем совпадения по логину в базе
    user = user_query.first()
    if user:   # Если совпадение нашлось
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Аккаунт с данным логином уже существует')
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Пароли не совпадают')
    mail_check_query = db.query(Models.User).filter(
        Models.User.email == payload.email.lower())
    if mail_check_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='На эту почту уже зарегистрирован аккаунт')
    # Хэширование пароля
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm  # совпадают ли пароли
    # записываем нового пользователя
    new_user = Models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # обновили данные

    try:
        # Отправляем код подтверждения на почту
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        user_query.update(
            {'verification_code': verification_code}, synchronize_session=False)

        await email.send_auth_code(new_user.email, verification_code)
        db.commit()
    except Exception as error:
        print('Error', error)
        user_query.update(
            {'verification_code': None}, synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Возникли проблемы с отправкой кода на почту')
    return {'status': 'success', 'message': 'Пользователь успешно зарегистрирован'}


@router.post('/login')
def login(payload: userSchemas.LoginUserSchema, response: Response, db: Session = Depends(get_db),
          Authorize: AuthJWT = Depends()):
    # Check if the user exist
    user = db.query(Models.User).filter(
        Models.User.login == payload.login.lower()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Неверный логин или пароль')
    # Check if the password is valid
    if not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Неверный логин или пароль')

    # Создаем access token
    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Создаем refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Кладем refresh и access tokens в cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Check if user verified his email
    if not user.verified:
        return {'status': 'Успешно', 'access_token': access_token, 'message': 'Пожалуйста, подтвердите вашу почту'}
    # Send both access
    return {'status': 'Успешно', 'access_token': access_token, 'message': ''}


@router.get('/refresh')
def refresh_token(response: Response, request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = db.query(Models.User).filter(Models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}