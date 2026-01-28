
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    business_id = Column(ForeignKey("business.id"))
    