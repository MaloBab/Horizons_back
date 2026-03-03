from sqlalchemy import Column, Integer, String
from .base import Base

class Preference(Base):
    # Represents a grouping of categories
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String, nullable=False, unique=True)