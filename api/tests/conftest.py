"""
Fixtures partagées pour les tests de l'API Python.
Utilise une base SQLite en mémoire pour isoler les tests de la BDD de production.
"""

import os
import sys
import types
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock des variables d'environnement
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")

# Mock psycopg2 AVANT tout import de db.database
psycopg2_mock = types.ModuleType("psycopg2")
psycopg2_mock.Error = Exception
psycopg2_mock.connect = MagicMock()
psycopg2_mock.paramstyle = "pyformat"
psycopg2_mock.apilevel = "2.0"
psycopg2_mock.threadsafety = 2
sys.modules["psycopg2"] = psycopg2_mock
sys.modules["psycopg2.extensions"] = types.ModuleType("psycopg2.extensions")
sys.modules["psycopg2.extras"] = types.ModuleType("psycopg2.extras")

# Créer le moteur SQLite de test AVANT d'importer db.database
# check_same_thread=False est nécessaire car FastAPI TestClient utilise des threads différents
_test_engine = create_engine(
    "sqlite:///:memory:",
    echo=False,
    connect_args={"check_same_thread": False},
)
_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

# Patcher db.database pour utiliser SQLite au lieu de PostgreSQL
import db.database as db_module
db_module.engine = _test_engine
db_module.SessionLocal = _TestSessionLocal

# Maintenant importer Base (qui utilise notre engine patché)
from db.database import Base

# Créer les tables immédiatement pour que les imports de routers fonctionnent
Base.metadata.create_all(bind=_test_engine)


@pytest.fixture(scope="session")
def test_engine():
    return _test_engine


@pytest.fixture(scope="session")
def tables(test_engine):
    """Tables déjà créées au niveau du module, cette fixture sert de marqueur."""
    yield


@pytest.fixture
def db_session(test_engine, tables):
    """Fournit une session de test avec nettoyage complet entre chaque test."""
    session = _TestSessionLocal()
    yield session
    session.rollback()
    # Nettoyer toutes les tables pour éviter les conflits entre tests
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture
def sample_user(db_session):
    """Crée un utilisateur de test dans la BDD."""
    from schemas.model import User
    user = User(id=1, uid="test-user-uid-123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_user_with_codes(db_session, sample_user):
    """Crée un utilisateur avec des codes comptables préexistants."""
    from schemas.model import UserCodeMap, UserCodeGenAux, UserJournal

    code_map = UserCodeMap(
        user_id=sample_user.id,
        code_map={
            "001 SURGELE": "601100",
            "002 ALIMENTAIRE": "601100",
            "003 EMBALLAGE": "602201",
        }
    )
    code_gen_aux = UserCodeGenAux(
        user_id=sample_user.id,
        code_map_gen_aux={
            "Code General 401000": "401000",
            "Code Auxilliaire 401000": "401LR",
        }
    )
    journal = UserJournal(
        user_id=sample_user.id,
        journal_map={"Journal": "ACM"}
    )

    db_session.add_all([code_map, code_gen_aux, journal])
    db_session.commit()

    return sample_user


@pytest.fixture
def mock_logger():
    """Fournit un logger mock pour les tests."""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.error = MagicMock()
    logger.warning = MagicMock()
    logger.debug = MagicMock()
    return logger


@pytest.fixture
def tmp_upload_dir(tmp_path):
    """Crée une structure de répertoires temporaires pour les uploads."""
    upload_dir = tmp_path / "uploads"
    download_dir = tmp_path / "downloads"
    upload_dir.mkdir()
    download_dir.mkdir()
    return upload_dir, download_dir


@pytest.fixture
def sample_edi_content():
    """Contenu EDI de test pour les conversions."""
    # Le fichier EDI doit contenir "EDI" dans la première ligne
    # et les lignes se terminent par une apostrophe
    return (
        "UNB+UNOA:2+EDI+5412345678908:14+8798765432106:14+230615:1245+00000000000123'\n"
        "UNH+1+INVOIC:D:96A:UN:EAN008'\n"
        "BGM+380+INV-2023-001+9'\n"
        "DTM+137:20230615:102'\n"
        "RFF+GN:MAGASIN_TEST'\n"
        "NAD+BY+5412345678908::9'\n"
        "IMD+F++:::Article test 1'\n"
        "MOA+203:150.00'\n"
        "IMD+F++:::Article test 2'\n"
        "MOA+203:250.00'\n"
        "UNS+S'\n"
        "MOA+39:400.00'\n"
        "MOA+124:80.00'\n"
        "MOA+218:0.00'\n"
        "UNT+20+1'\n"
        "UNZ+1+00000000000123'\n"
    )


@pytest.fixture
def sample_edi_file(tmp_upload_dir, sample_edi_content):
    """Crée un fichier EDI de test."""
    upload_dir, _ = tmp_upload_dir
    edi_file = upload_dir / "test_facture.txt"
    edi_file.write_text(sample_edi_content, encoding="ISO-8859-1")
    return str(edi_file)
