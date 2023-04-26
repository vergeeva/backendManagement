import hashlib
from datetime import timedelta
from random import randbytes

from fastapi import APIRouter, Request, Response, status, Depends, HTTPException

from app import oauth2
from .. import Models, utils
from ..Schemas import userSchemas
from sqlalchemy.orm import Session
from ..database import get_db
from app.oauth2 import AuthJWT
from ..config import settings
# from ..email import send_email_async


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: userSchemas.CreateUserSchema, request: Request, db: Session = Depends(get_db)):
    user_query = db.query(Models.User).filter(
        Models.User.login == payload.login.lower())
    user = user_query.first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    mail_check_query = db.query(Models.User).filter(
        Models.User.email == payload.email.lower())
    if mail_check_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account with this email already exist')
    # Хэширование пароля
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    new_user = Models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        # Отправляем код подтверждения на почту
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        user_query.update(
            {'verification_code': verification_code}, synchronize_session=False)
        db.commit()
        url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/api/auth/verifyemail/{token.hex()}"
        # await send_email_async("Верификация аккаунта на сайте", new_user.email, {
        #     'title': 'Привет, новый пользователь!',
        #     'name': f'Код: {verification_code}'
        # })
    except Exception as error:
        print('Error', error)
        user_query.update(
            {'verification_code': None}, synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error sending email')
    return {'status': 'success', 'message': 'The user has been successfully registered'}


@router.post('/login')
def login(payload: userSchemas.LoginUserSchema, response: Response, db: Session = Depends(get_db),
          Authorize: AuthJWT = Depends()):
    # Check if the user exist
    user = db.query(Models.User).filter(
        Models.User.login == payload.login.lower()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # Check if user verified his email
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please verify your email address')

    # Check if the password is valid
    if not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token}


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


@router.get('/verifyemail/{token}')
def verify_me(token: str, db: Session = Depends(get_db)):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()
    user_query = db.query(Models.User).filter(
        Models.User.verification_code == verification_code)
    db.commit()
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid code or user doesn't exist")
    if user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Email can only be verified once')
    user_query.update(
        {'verified': True, 'verification_code': None}, synchronize_session=False)
    db.commit()
    return {
        "status": "success",
        "message": "Account verified successfully"
    }
