
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.task.model import Task
    from app.course.model import Course


class Quiz(Base):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    course_id = Column(ForeignKey("course.id", ondelete="CASCADE"))

    course = relationship("Course", back_populates="quizzes") 
    tasks = relationship("Task", back_populates="quiz", cascade="all, delete-orphan")