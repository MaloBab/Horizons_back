from sqlalchemy import Column, Integer, String
from .base import Base

class Category(Base):
    # Represents a category of jobs (e.g. "Accueil", "Restauration", etc.)
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String, nullable=False, unique=True)