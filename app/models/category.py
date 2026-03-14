from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    label: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    responsible: Mapped[str | None] = mapped_column(String, nullable=True)