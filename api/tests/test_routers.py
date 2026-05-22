"""
Tests unitaires pour api/routers.py
Couvre : les endpoints API via FastAPI TestClient
Note: Les tests d'endpoint nécessitent que le thread check_new_users
      soit patché pour éviter les side effects au chargement du module.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Patch le threading et la création de tables AVANT d'importer routers/main
import threading
_original_thread_start = threading.Thread.start
threading.Thread.start = lambda self: None  # Désactive le thread daemon

from fastapi.testclient import TestClient
from main import app
from routers import get_session

# Restaurer après import
threading.Thread.start = _original_thread_start


@pytest.fixture
def client(db_session):
    """Crée un TestClient FastAPI avec BDD de test."""
    def override_get_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


class TestStatusEndpoint:
    """Tests pour l'endpoint /api/status."""

    def test_status_without_user_cookie(self, client):
        """Doit retourner un statut OK sans info utilisateur."""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["user"] is None

    def test_status_with_user_cookie(self, client):
        """Doit retourner le statut avec l'info utilisateur."""
        response = client.get("/api/status", cookies={"userId": "test-user-uid-123"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["user"] == "test-user-uid-123"


class TestCodesEndpoint:
    """Tests pour les endpoints /api/codes."""

    def test_get_codes_without_cookie(self, client):
        """Doit retourner 401 sans cookie userId."""
        response = client.get("/api/codes")
        assert response.status_code == 401

    def test_get_codes_nonexistent_user(self, client, sample_user):
        """Doit retourner 404 pour un utilisateur inexistant."""
        response = client.get("/api/codes", cookies={"userId": "nonexistent"})
        assert response.status_code == 404

    def test_get_codes_existing_user(self, client, sample_user_with_codes):
        """Doit retourner les codes pour un utilisateur existant."""
        response = client.get(
            "/api/codes",
            cookies={"userId": sample_user_with_codes.uid}
        )
        assert response.status_code == 200
        data = response.json()
        assert "comptas" in data
        assert "other" in data
        assert "journal" in data

    def test_post_codes_without_cookie(self, client):
        """Doit retourner 401 sans cookie userId."""
        response = client.post("/api/codes", json={"comptas": {"key": "val"}})
        assert response.status_code == 401

    def test_post_codes_empty_update(self, client, sample_user_with_codes):
        """Doit retourner une erreur si aucun code n'est fourni."""
        response = client.post(
            "/api/codes",
            json={},
            cookies={"userId": sample_user_with_codes.uid}
        )
        # Le endpoint retourne 400 ou 500 selon que le json vide est parsé
        assert response.status_code in (400, 500)


class TestCodeComptasLegacyEndpoint:
    """Tests pour les endpoints legacy /api/codecomptas."""

    def test_get_codecomptas_existing_user(self, client, sample_user_with_codes):
        """Doit retourner les codes comptables."""
        response = client.get(
            "/api/codecomptas",
            cookies={"userId": sample_user_with_codes.uid}
        )
        assert response.status_code == 200
        data = response.json()
        assert "001 SURGELE" in data


class TestJournalLegacyEndpoint:
    """Tests pour les endpoints legacy /api/journal."""

    def test_get_journal_existing_user(self, client, sample_user_with_codes):
        """Doit retourner le journal."""
        response = client.get(
            "/api/journal",
            cookies={"userId": sample_user_with_codes.uid}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Journal" in data
        assert data["Journal"] == "ACM"


class TestCleanupEndpoint:
    """Tests pour l'endpoint /api/cleanup."""

    def test_cleanup_without_cookie(self, client):
        """Doit retourner 401 sans cookie userId."""
        response = client.post("/api/cleanup")
        assert response.status_code == 401

    def test_cleanup_with_no_temp_files(self, client):
        """Doit retourner un message quand il n'y a pas de fichiers temporaires."""
        response = client.post("/api/cleanup", cookies={"userId": "clean-user"})
        assert response.status_code == 200
        data = response.json()
        assert "No temporary files found" in data["message"]


class TestConversionEndpoint:
    """Tests pour l'endpoint /api/conversion."""

    def test_conversion_without_cookie(self, client):
        """Doit retourner 401 sans cookie userId."""
        response = client.post(
            "/api/conversion",
            files=[("files", ("test.txt", b"data", "text/plain"))]
        )
        assert response.status_code == 401

    def test_conversion_nonexistent_user(self, client, sample_user):
        """Doit retourner 404 pour un utilisateur inexistant."""
        response = client.post(
            "/api/conversion",
            files=[("files", ("test.txt", b"data", "text/plain"))],
            cookies={"userId": "nonexistent"},
        )
        assert response.status_code == 404

    def test_conversion_non_txt_file_rejected(self, client, sample_user_with_codes):
        """Doit retourner 400 si aucun fichier .txt n'est fourni."""
        response = client.post(
            "/api/conversion",
            files=[("files", ("test.xlsx", b"data", "application/octet-stream"))],
            cookies={"userId": sample_user_with_codes.uid},
        )
        assert response.status_code == 400
