from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.models import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.__dict__)
        return JSONResponse(content=token, status_code=200)
    else:
        return JSONResponse(content={"message":"The data don't match."},status_code=404)