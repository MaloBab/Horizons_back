import enum
from .base import Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    google_sub = Column(String, unique=True, nullable=True, index=True)
    role = Column( Enum(UserRole), default=UserRole.user, nullable=False)
    profile_picture_url = Column(String, nullable=True)
    calendar_id = Column(String, nullable=True)
    
    activities = relationship("Activity", back_populates="author")