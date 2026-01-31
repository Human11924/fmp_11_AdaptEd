
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.quiz.model import Quiz


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")