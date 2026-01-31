from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.quiz.model import Quiz


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    correct_ans = Column(String, nullable=False)
    incorrect_1 = Column(String)
    incorrect_2 = Column(String)
    incorrect_3 = Column(String)
    incorrect_4 = Column(String)
    incorrect_5 = Column(String)
    quiz_id = Column(ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)

    quiz = relationship("Quiz", back_populates="tasks")