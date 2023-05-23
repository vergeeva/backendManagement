import hashlib
from random import randbytes
from typing import List

from fastapi import BackgroundTasks, FastAPI, APIRouter, HTTPException, status, Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import Models
from app.config import settings
from app.database import get_db
from app.oauth2 import require_user


class EmailSendMessageSchema(BaseModel):
    email: EmailStr
    code: str

    class Config:
        orm_mode = True


conf = ConnectionConfig(
    MAIL_USERNAME="vergeeva-time-management",
    MAIL_PASSWORD="aqbsacbmiaojjfdp",
    MAIL_FROM="vergeeva-time-management@yandex.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

router = APIRouter()
html = """
<p>Ваш код подтверждения: </p> 
"""


async def send_auth_code(email: EmailStr, code: str) -> JSONResponse:
    message = MessageSchema(
        subject="Верификация аккаунта на сайте по тайм-менеджменту",
        recipients=[email],
        body=html + f'<p>{code}</p>',
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Сообщение было отправлено"})


@router.get("/verify_profile") # Для отправки сообщения для зарегистрированного пользователя
async def verify_profile_mail(user_id: str = Depends(require_user), db: Session = Depends(get_db)) -> JSONResponse:
    user_query = db.query(Models.User).filter(Models.User.id == user_id)  # Запрос на поиск текущего пользователя
    user = user_query.first()  # Берем данные записи пользователя
    try:
        # Отправляем код подтверждения на почту
        # генерируем код
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        # записываем в бд в строку текущего пользователя
        user_query.update(
            {'verification_code': verification_code}, synchronize_session=False)
        db.commit()  # отправляем изменения в бд
        await send_auth_code(user.email, verification_code)  # используем асинхронную функцию отправки
    except Exception as error:  # если что-то пошло не так
        print('Error', error)  # печатаем ошибку в консоль Python
        user_query.update(
            {'verification_code': None}, synchronize_session=False)  # Очищаем поле кода в таблице
        db.commit()  # сохраняем изменения
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Произошла ошибка с отправкой письма на почту')
    # отправляем ответ о состоянии выполнения программы
    return JSONResponse(status_code=200, content={"message": "Сообщение было отправлено"})


@router.get("/verify_auth_code/{user_specified_code}")  # проверка введенного зарегистрированного пользователя кода
async def verify_profile_mail(user_specified_code: str,
                              db: Session = Depends(get_db), user_id: str = Depends(require_user)) -> JSONResponse:
    user_query = db.query(Models.User).filter(Models.User.id == user_id)
    user = user_query.first()  # запрос в бд и взятие объекта пользователь
    if not user:  # если такого не нашлось в базе
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    if user.verification_code == user_specified_code:  # если коды совпали
        user_query.update(  # стираем код в базе, ведь в нем нет нужды больше
            {'verified': True, 'verification_code': None}, synchronize_session=False)
        db.commit()  # отправляем изменения
        return JSONResponse(status_code=200, content={"message": "Почта успешно подтверждена"})
        # возвращаем сообщение об успешном выполнении
    else:  # если коды не совпали, то сообщаем в виде json об этом
        return JSONResponse(status_code=200, content={"message": "Неверный код подтверждения! Проверьте ввод"})


@router.post("/verify_mail_not_auth")  # проверка введенного незарегистрированного пользователя кода
async def verify_profile_not_auth(email: EmailSendMessageSchema,
                              db: Session = Depends(get_db)) -> JSONResponse:
    user_query = db.query(Models.User).filter(Models.User.email == email.email)
    user = user_query.first()  # запрос в бд и взятие объекта пользователь
    if not user:  # если такого не нашлось в базе
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    if user.verification_code == email.code:  # если коды совпали
        user_query.update(  # стираем код в базе, ведь в нем нет нужды больше
            {'verified': True, 'verification_code': None}, synchronize_session=False)
        db.commit()  # отправляем изменения
        return JSONResponse(status_code=200, content={"message": "Почта успешно подтверждена"})
        # возвращаем сообщение об успешном выполнении
    else:  # если коды не совпали, то сообщаем в виде json об этом
        return JSONResponse(status_code=200, content={"message": "Неверный код подтверждения! Проверьте ввод"})