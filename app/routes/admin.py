from fastapi import APIRouter, Form
from typing import Annotated
from sqlalchemy.orm import session

from app.schemas.admin_schema import RegisterAdminRequest
from app.utils.dbdependency import get_db

router = APIRouter()

# @router.post('/register-admin')
# def register_admin(
#     request: Annotated[RegisterAdminRequest,Form()],
#     db: session = Depends(get_db)
# ):
    

@router.get('/test')
async def some_random_func():
    return {'message':"Namaskaram"}