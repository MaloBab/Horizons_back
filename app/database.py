import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(override=True)

# L'adresse de la base de données. 
# (ex: "postgresql://utilisateur:motdepasse@IP_DU_RASPBERRY/nom_de_la_base")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Affiche l'URL pour vérifier qu'elle est bien chargée

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL n'est pas défini dans le fichier .env")

# Le "moteur" qui va exécuter le code SQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# La "session" est ce qui permet de discuter avec la base (ajouter, lire, etc.)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La classe de base dont tous tes modèles vont hériter
Base = declarative_base()

# Fonction pour obtenir une session de base de données à chaque requête, 
# puis la fermer proprement quand la requête est terminée.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
