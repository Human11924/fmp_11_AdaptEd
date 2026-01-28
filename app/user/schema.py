from pydantic_settings import BaseSettings


class SUser_register(BaseSettings):
    first_name:str
    last_name:str
    email:str
    hashed_password:str

class SUser_login(BaseSettings):
    email:str
    hashed_password:str

class SUser_profile(BaseSettings):
    first_name:str
    last_name:str
    email:str