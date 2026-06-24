from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    display_name = Column(String(50), nullable=False)

    projects = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
    )