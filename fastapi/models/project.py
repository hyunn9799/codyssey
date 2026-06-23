from datetime import datetime

from sqlalchemy import Column,DateTime,ForeignKey,Integer,String,Text
from sqlalchemy.orm import relationship

from database import Base

class Project(Base):
    __tablename__="projects"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text,nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="projects")

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all,delete-orphan",
    )