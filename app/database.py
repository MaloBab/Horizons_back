import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# L'adresse de la base de données. 
# (ex: "postgresql://utilisateur:motdepasse@IP_DU_RASPBERRY/nom_de_la_base")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Le "moteur" qui va exécuter le code SQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# La "session" est ce qui permet de discuter avec la base (ajouter, lire, etc.)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La classe de base dont tous tes modèles vont hériter
Base = declarative_base()