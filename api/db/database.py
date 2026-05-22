from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from contextlib import contextmanager


def get_db_url():
    """
    Récupère les paramètres de connexion depuis les variables d'environnement
    et construit l'URL de connexion PostgreSQL
    """
    try:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        
        if not all([host, port, database, user, password]):
            raise ValueError("Variables d'environnement manquantes pour la connexion DB")
            
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    except Exception as e:
        print(f"Erreur lors de la construction de l'URL de connexion: {e}")
        raise



try:
    DATABASE_URL = get_db_url()
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Erreur lors de l'initialisation de SQLAlchemy: {e}")
    raise




@contextmanager
def get_db_connection():
    """Context manager pour la connexion psycopg2"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        yield conn
    except psycopg2.Error as e:
        print(f"Erreur de connexion PostgreSQL: {e}")
        raise
    finally:
        if conn:
            conn.close()
            print("Connexion fermée")

def get_session():
    """Génère une nouvelle session SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Teste la connexion à la base de données"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            print("Connexion à la base de données réussie!")
            return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False