from typing import Optional

from aiosmtplib.smtp import DEFAULT_TIMEOUT
from pydantic import BaseSettings, EmailStr, DirectoryPath


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    MAIL_USERNAME = str
    MAIL_PASSWORD = str
    MAIL_FROM = str
    MAIL_PORT = int
    MAIL_SERVER = str
    MAIL_STARTTLS = bool
    MAIL_SSL_TLS = bool
    USE_CREDENTIALS = bool
    VALIDATE_CERTS = bool

    class Config:
        env_file = './.env'


settings = Settings()
