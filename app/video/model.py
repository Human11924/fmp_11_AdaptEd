

from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class Video(Base):
    __tablename__ = "video"
    id = Column(Integer , primary_key = True)
    title = Column(String)
    url = Column(String)
    duration = Column(Integer)
    course_id = Column(ForeignKey("course.id"))