
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")