import enum
from sqlalchemy import Column, Integer, String, UUID, Enum
from database import Base

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class Users(Base):
    __tablename__ = "users" # Le vrai nom de la table dans la base

    # On définit les colonnes
    id = Column(UUID, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column( Enum(UserRole), default=UserRole.user, nullable=False)
    profile_picture_url = Column(String, nullable=True)