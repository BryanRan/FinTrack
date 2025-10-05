from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# Initialisation du chemin
BASE_DIR = Path(__file__).resolve().parent.parent.parent # Racine du projet
DB_PATH = BASE_DIR/"database"/"fintrack.db" # Emplacement de la bd

SQL_ALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Creation d'un moteur pour la BD
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
) # Connexion entre SQL_ALCHEMY et la base

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) # Générer des sessions de BD

Base = declarative_base() #  Pour faire des requêtes SQL déclarative (ORM)   