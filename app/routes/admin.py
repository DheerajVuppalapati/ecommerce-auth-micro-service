from datetime import  timedelta 
from typing import Annotated
from pathlib import Path
import os
from dotenv import load_dotenv

from fastapi import APIRouter, Form, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from jwt.exceptions import InvalidTokenError


from app.schemas.admin_schema import RegisterAdminRequest,AdminResponse,Token
from app.utils.dbdependency import get_db
from app.models.userModel import User
from app.utils.auth_helpers import verify_password,hash_password,create_access_token,authenticate_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

@router.post('/register-super-admin')
async def register_admin(
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
    

@router.post('/token')
async def login_for_access_token(
    db: Annotated[Session, Depends(get_db)],
    request: OAuth2PasswordRequestForm = Depends()
) -> Token:
    try:
        user = authenticate_user(db, request.username, request.password)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )

        # Fix: get int value from env var
        expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
        access_token = create_access_token(
            data={"sub": user.username},
            expire_delta=timedelta(minutes=expire_minutes)
        )

        return Token(
            access_token = access_token,
            token_type = "bearer"
        )

    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get('/test')
async def some_random_func():
    return {'message':"Namaskaram"}