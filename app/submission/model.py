from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base


class Submission(Base):
    __tablename__ = "submission"

    id = Column(Integer, primary_key=True, index=True)
    submission_date = Column(DateTime)
    submission_status = Column(String, default=False)
    task_id = Column(Integer, ForeignKey("task.id"))

