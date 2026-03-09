from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud
from ..core import security
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth = OAuth()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Authentifie l'utilisateur et génère un jeton JWT."""

    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user:
        user = crud.user.get_user_by_username(db, username=form_data.username)
        
    if not user or not security.verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(subject=user.id, expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": access_token, "token_type": "bearer"}