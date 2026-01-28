from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER:str
    DB_HOST:str
    DB_PASS:str
    DB_NAME:str
    DB_PORT:int
    GEMINI_API_KEY:str
    secret_key:str
    algorithm:str
    
    class Config:
        env_file = ".env"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
DB_settings = Settings()
db_url = DB_settings.db_url
print(db_url)