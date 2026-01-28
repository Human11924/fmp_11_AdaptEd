
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer , primary_key = True)
    first_name = Column(String)
    second_name = Column(String)
    phone_number = Column(String , nullable=True)
    email = Column(String)
    hashed_password = Column(String)
    course_id = Column(ForeignKey("course.id"))
    