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
from app.utils.auth_helpers import hash_password

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

@router.post('/api/auth/register-user')
async def register_user(
    db: Annotated[Session,Depends(get_db)],
    request: Annotated[RegisterUserRequest,Form()]
) -> UserResponse:
    try:
        email = request.email
        mobile_number = request.mobile_number
        username = request.username

        user_exists = db.query(User).filter(User.username  == username).first() 
        email_exists = db.query(User).filter(User.email == email).first()
        mobile_number_exists = db.query(User).filter(User.mobile_number == mobile_number).first() 

        if user_exists: 
            raise HTTPException(status_code = 409, detail='The username is already taken')
        if email_exists:
            raise HTTPException(status_code = 409, detail='The given email id is already taken')
        if mobile_number_exists:
            raise HTTPException(status_code = 409, detail='The given mobile number is already taken')
        
        if not user_exists and not email_exists and not mobile_number_exists:
            hashed_pass = hash_password(request.password_hash)
            new_user = User(
                first_name = request.first_name,
                last_name = request.last_name,
                username = request.username,
                email = request.email,
                mobile_number = request.mobile_number,
                password_hash = hashed_pass
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return UserResponse(
                user_id = new_user.user_id,
                username = new_user.username,
                email = new_user.email,
                role_name = new_user.role.role_name,
                status = new_user.status
            )
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"An error occured: {str(e)}")
