

from sqlalchemy import Column, Integer, String
from app.database import Base


class Business(Base):
    __tablename__ = "business"
    id = Column(Integer , primary_key = True)
    name = Column(String)
    password = Column(String)