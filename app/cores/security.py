from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "my_secret_key_this_is"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password:str) -> str:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data:dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp":datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
