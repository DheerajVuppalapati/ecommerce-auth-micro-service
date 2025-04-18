from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Form, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.schemas.admin_schema import RegisterAdminRequest,AdminResponse
from app.utils.dbdependency import get_db
from app.models.userModel import User

load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

def hash_password(password):
    return pwd_context.hash(password)


@router.post('/register-admin')
def register_admin(
    request: Annotated[RegisterAdminRequest,Form()],
    db: Annotated[Session,Depends(get_db)]
) -> AdminResponse:
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
                role_id = request.role_id,
                password_hash = hashed_pass
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return AdminResponse(
                user_id = new_user.user_id,
                username = new_user.username,
                email = new_user.email,
                role_name = new_user.role.role_name,
                status = new_user.status
            )
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"An error occured: {str(e)}")
    
  


@router.get('/test')
async def some_random_func():
    return {'message':"Namaskaram"}