from datetime import datetime
from sqlalchemy import Boolean, Column , DateTime , Integer, String, Text
from database import Base

from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title=Column(String(100), nullable=False)
    description=Column(Text, nullable=True)
    is_done = Column(Boolean,default=False)
    due_date = Column(String(10),nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 

    project = relationship("Project",back_populates="tasks")
