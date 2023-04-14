from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy import TIMESTAMP, Column
import datetime
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        default=datetime.datetime.utcnow
    )

    update_at = Column(
        TIMESTAMP,
        nullable=True,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f'{self.__class__.__name__}'