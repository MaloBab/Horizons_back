from fastapi import FastAPI
import models
from database import SessionLocal, engine

# Demande à SQLAlchemy de créer les tables dans la base de données
# (Si elles existent déjà, il ne fait rien)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Fonction pour obtenir une session de base de données à chaque requête, 
# puis la fermer proprement quand la requête est terminée.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- DÉBUT DES ROUTES ---

# 1. Une route simple pour vérifier que le serveur tourne (Méthode GET)
@app.get("/")
def lire_racine():
    return {"message": "Bienvenue sur mon super backend !"}