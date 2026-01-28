

from fastapi import APIRouter, Depends, HTTPException, Response
from app.database import async_session_maker
from app.user.auth import create_access_token
from app.user.dependencies import get_current_user
from app.user.model import User
from app.user.schema import SUser_login, SUser_profile, SUser_register
from app.user.user_dao import User_dao

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)


@router.post("/register")
async def register_user(get_user:SUser_register):
    user = await User_dao.find_one_or_none(email = get_user.email)
    if user:
        raise HTTPException(500  , detail= "You are already registered")
    await User_dao.add(
        first_name = get_user.first_name,
        last_name = get_user.last_name,
        email = get_user.email,
        hashed_password = get_user.hashed_password,
    )
@router.post("/login")
async def login_user(response:Response , set_user:SUser_login):
    user = await User_dao.find_one_or_none(email = set_user.email , hashed_password = set_user.hashed_password)
    if not user:
        raise HTTPException(500 , detail = "login or password is incorrect")
    if user:
        access_token = create_access_token({"sub":str(user.id)})
        response.set_cookie("user_access_token" , access_token , httponly=True)
        return access_token
    
@router.get("/profil", response_model= SUser_profile)
async def user_profile(current_user = Depends(get_current_user)):
    return current_user