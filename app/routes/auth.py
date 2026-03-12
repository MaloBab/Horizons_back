from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud
from ..core import security
from ..core.oauth_codes import generate_code, consume_code
from ..database import get_db
from ..schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ── OAuth Google setup ───────────────────────────────────────────────────────
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


# ── Login classique ──────────────────────────────────────────────────────────
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authentifie l'utilisateur et génère un jeton JWT."""
    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user:
        user = crud.user.get_user_by_username(db, username=form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ce compte utilise la connexion Google. Connectez-vous via Google ou définissez un mot de passe depuis votre profil.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not security.verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ── Google OAuth — étape 1 : redirect ───────────────────────────────────────
@router.get("/google")
async def google_login(request: Request):
    """Redirige l'utilisateur vers la page de consentement Google."""
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


# ── Google OAuth — étape 2 : callback ───────────────────────────────────────
@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Reçoit le code Google, récupère le profil, crée ou retrouve le compte,
    puis redirige le frontend avec un code jetable (30s, one-shot).

    Cas gérés :
      - Nouvel utilisateur Google  → création du compte (sans password_hash)
      - Compte existant par email  → liaison transparente, connexion directe
      - Compte Google déjà connu   → connexion directe
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="Échec de l'authentification Google.")

    userinfo = token.get("userinfo") or await oauth.google.userinfo(token=token)
    email: str = userinfo["email"]
    google_sub: str = userinfo["sub"]
    given_name: str = userinfo.get("given_name", "")
    name: str = userinfo.get("name", email.split("@")[0])

    # 1. Cherche par google_sub (utilisateur déjà OAuth)
    user = crud.user.get_user_by_google_sub(db, google_sub=google_sub)

    if not user:
        # 2. Cherche par email (compte classique avec même adresse Gmail)
        user = crud.user.get_user_by_email(db, email=email)
        if user:
            # Liaison du compte existant avec Google
            crud.user.link_google_account(db, user=user, google_sub=google_sub)
        else:
            # 3. Nouveau compte — pas de mot de passe
            username = _unique_username(db, given_name or name)
            user = crud.user.create_oauth_user(
                db,
                UserCreate(username=username, email=email, password=""),
                google_sub=google_sub,
            )

    jwt = security.create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Code jetable à la place du JWT dans l'URL
    code = generate_code(jwt)
    return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?code={code}")


# ── Échange du code contre le JWT ───────────────────────────────────────────
@router.post("/google/exchange")
def exchange_code(payload: dict):
    """
    Reçoit le code jetable, retourne le JWT.
    Le code est valable 30 secondes et ne peut être utilisé qu'une fois.
    """
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code manquant.")

    jwt = consume_code(code)
    if not jwt:
        raise HTTPException(status_code=400, detail="Code invalide ou expiré.")

    return {"access_token": jwt, "token_type": "bearer"}


# ── Helpers ──────────────────────────────────────────────────────────────────
def _unique_username(db: Session, base: str) -> str:
    """Génère un username unique basé sur le prénom Google."""
    slug = base.lower().replace(" ", "_")[:20]
    candidate = slug
    counter = 1
    while crud.user.get_user_by_username(db, username=candidate):
        candidate = f"{slug}_{counter}"
        counter += 1
    return candidate