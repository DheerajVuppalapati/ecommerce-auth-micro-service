from pydantic import BaseModel, EmailStr
from uuid import UUID



class RegisterAdminRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    mobile_number: str
    role_id: int
    password_hash: str

class AdminResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role_name: str
    status: str

class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    mobile_number: str
    password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role_name: str
    status: str
