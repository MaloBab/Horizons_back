from sqlalchemy.orm import mapped_column, Mapped
from .base import Base

class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    day_index: Mapped[int]
    start_time: Mapped[int]
    end_time: Mapped[int]