
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Quiz(Base):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    course_id = Column(ForeignKey("course.id", ondelete="CASCADE"))

    course = relationship("Course", back_populates="quizzes") 