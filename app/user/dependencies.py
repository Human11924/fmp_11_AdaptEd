from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from app.config import Settings
from app.user.user_dao import User_dao
  
settings = Settings()

def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if token:
        return token
    raise HTTPException(500, detail="couldn't take access token")
    


async def get_current_user(token: str = Depends(get_access_token)):

    access = jwt.decode(
        token,
        settings.secret_key,
        algorithms=settings.algorithm
    )

    user_id:str = access.get("sub")
    user = await User_dao.find_one_or_none(id=int(user_id))

    if user:
        return user
    raise HTTPException(500, detail="couldn't take user after jwt token decode")
