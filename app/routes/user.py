from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pathlib import Path

import jwt
from fastapi import APIRouter, Form, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.schemas.admin_schema import RegisterUserRequest,UserResponse,Token
from app.utils.dbdependency import get_db
from app.models.userModel import User

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

