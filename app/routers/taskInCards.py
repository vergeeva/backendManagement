import uuid

from fastapi import APIRouter, Depends, status, APIRouter, Response, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import Models
from ..Schemas import kanbanSchemas
from app.oauth2 import require_user

router = APIRouter()