import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from ..database import get_db
from .. import crud, schemas

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 240))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY n'est pas définie dans le fichier .env")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    if not SECRET_KEY :
        raise ValueError("SECRET_KEY n'est pas définie dans le fichier .env")
    
    if not ALGORITHM:
        raise ValueError("ALGORITHM n'est pas définie dans le fichier .env")
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Déchiffre le token JWT, extrait l'ID de l'utilisateur et le cherche en base.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        
        if SECRET_KEY is None or ALGORITHM is None:
            raise ValueError("SECRET_KEY ou ALGORITHM n'est pas définie dans le fichier .env")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id_str: str = str(payload.get("sub"))
        if user_id_str is None:
            raise credentials_exception
            
        try:
            token_data = UUID(user_id_str)
        except ValueError:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    user = crud.user.get_user(db, user_id=token_data)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user = Depends(get_current_user)):
    """
    Vérifie que l'utilisateur connecté possède bien le rôle 'admin'.
    Utilise get_current_user en amont pour valider le jeton.
    """

    if current_user.role != "admin" and getattr(current_user.role, 'value', current_user.role) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits d'administrateur pour effectuer cette action."
        )
    return current_user