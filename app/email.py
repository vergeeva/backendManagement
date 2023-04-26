# import os
# from fastapi import BackgroundTasks
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
#
# from dotenv import load_dotenv
# load_dotenv('.env')
#
# class Envs:
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
#     MAIL_FROM = os.getenv('MAIL_FROM')
#     MAIL_PORT = os.getenv('MAIL_PORT')
#     MAIL_SERVER = os.getenv('MAIL_SERVER')
#     MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')
#
#     # MAIL_USERNAME=vergeeva-time-management
#     # MAIL_PASSWORD=aqbsacbmiaojjfdp
#     # MAIL_FROM=vergeeva-time-management@yandex.ru
#     # MAIL_PORT=465
#     # MAIL_SERVER=smtp.yandex.ru
#     # MAIL_FROM_NAME=vergeeva
#
#
# conf = ConnectionConfig(
#     MAIL_USERNAME=Envs.MAIL_USERNAME,
#     MAIL_PASSWORD=Envs.MAIL_PASSWORD,
#     MAIL_FROM=Envs.MAIL_FROM,
#     MAIL_PORT=Envs.MAIL_PORT,
#     MAIL_SERVER=Envs.MAIL_SERVER,
#     MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     TEMPLATE_FOLDER='./templates/email'
# )
#
#
# async def send_email_async(subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body,
#         subtype='html',
#     )
#
#     fm = FastMail(conf)
#
#     await fm.send_message(message, template_name='email.html')

from fastapi import FastAPI, APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
from pydantic import json

router = APIRouter()


class EmailSchema(BaseModel):
    email: EmailStr


@router.get("/send_mail")
async def send_mail(email: EmailSchema):
    template = """
        		<html>
        		<body>
            <p>Hi !!!
        		<br>Thanks for using fastapi mail, keep using it..!!!</p>
        		</body>
        		</html>
        		"""
    conf = ConnectionConfig(
        MAIL_USERNAME="vergeeva-time-management@yandex.ru",
        MAIL_PASSWORD="aqbsacbmiaojjfdp",
        MAIL_PORT=465,
        MAIL_SERVER="smtp.yandex.ru",
        MAIL_TLS=True,
        MAIL_SSL=False
    )
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)

    return {'json': JSONResponse(status_code=200, content={"message": "email has been sent"})}
