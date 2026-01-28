from jose import jwt
from app.config import Settings

settings = Settings()
def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode , settings.secret_key , algorithm=settings.algorithm
    )
    return encoded_jwt