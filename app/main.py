from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models

# Importation de tes routeurs
from .routes import auth
from .routes import user
from .routes import activity

# Cette ligne demande à SQLAlchemy de créer toutes les tables dans PostgreSQL 
# si elles n'existent pas encore sur ton Raspberry Pi.
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Horizons Open Sea Festival",
    description="Backend de gestion des bénévoles et plannings du festival.",
    version="1.0.0"
)

# Configuration CORS (Cross-Origin Resource Sharing)
# ⚠️ CORRECTION : On définit explicitement les origines autorisées
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # On utilise la liste explicite ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On connecte le routeur d'authentification à l'application principale
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(activity.router)

# Une petite route de test pour vérifier que le serveur tourne bien
@app.get("/", tags=["Health"])
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API Horizons Open Sea Festival !"}