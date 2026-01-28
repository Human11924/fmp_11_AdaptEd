
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class Course_User(Base):
    __tablename__ = "course_user"
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    correct_count = Column(Integer, default=0)

    