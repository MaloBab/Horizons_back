from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from enum import Enum

# On peut réutiliser l'Enum du modèle ou en redéfinir un pour Pydantic
class UserRole(str, Enum):
    admin = "admin"
    user = "user"

# 1. Champs communs (ce qu'on retrouve partout)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    profile_picture_url: Optional[str] = None

# 2. Champs nécessaires à la création (Inscription)
class UserCreate(UserBase):
    password: str # L'utilisateur envoie "password", mais on stockera "password_hash"

# 3. Champs nécessaires à la modification (Update)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    profile_picture_url: Optional[str] = None

# 4. Champs renvoyés par l'API (Lecture)
class UserResponse(UserBase):
    id: UUID
    role: UserRole

    class Config:
        from_attributes = True
        

# Pour les activités.
class UserShortResponse(BaseModel):
    username: str
    profile_picture_url: Optional[str] = None

    class Config:
        from_attributes = True