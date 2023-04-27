from typing import List

from fastapi import BackgroundTasks, FastAPI, APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from app.config import settings


class EmailSchema(BaseModel):
    email: List[EmailStr]


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


@router.get("/send_mail/{code}")
async def send_auth_code(email: EmailSchema, code: str) -> JSONResponse:
    message = MessageSchema(
        subject="Верификация аккаунта на сайте по тайм-менеджменту",
        recipients=email.dict().get("email"),
        body=html + f'<p>{code}</p>',
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
