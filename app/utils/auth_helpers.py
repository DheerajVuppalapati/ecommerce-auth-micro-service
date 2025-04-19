
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

import jwt
from passlib.context import CryptContext

from app.models.userModel import User

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data,expire_delta=None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    
    to_encode.update({"exp":expire})
    print(SECRET_KEY)
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    print(encode_jwt)
    return encode_jwt

def authenticate_user(db, username:str,password:str):
    user_dict = db.query(User).filter(User.username == username).first()
    if not user_dict:
        return False
    if not verify_password(password,user_dict.password_hash):
        return False
    return user_dict