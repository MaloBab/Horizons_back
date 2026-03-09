from sqlalchemy import Column, Integer
from .base import Base

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    day_of_week = Column(Integer, nullable=False)
    start_hour = Column(Integer, nullable=False)
    end_hour = Column(Integer, nullable=False)