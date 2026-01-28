

from fastapi import Depends, HTTPException, Request
from jose import jwt , JWTError
from app.config import Settings
from app.user.user_dao import User_dao
  
settings = Settings()

def get_access_token(request:Request):
    token = request.cookies.get("user_access_token")
    if token:
        return token
    else:
        raise HTTPException(500 , detail = "couldn't take access token")
    
print(get_access_token())