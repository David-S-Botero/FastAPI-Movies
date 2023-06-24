from jwt import encode, decode
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(data:dict) -> str:
    token:str = encode(payload=data, key=os.getenv('SECRET_KEY'), algorithm="HS256")
    return token

def validate_token(token:str) -> dict:
    data:dict = decode(token,os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return data

class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Not valid credentials")