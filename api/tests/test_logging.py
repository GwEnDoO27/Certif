"""
Tests unitaires pour api/Logging/logging_config.py
Couvre : configure_user_logging
"""

import os
import logging
import pytest
from Logging.logging_config import configure_user_logging


class TestConfigureUserLogging:
    """Tests pour la configuration du logging par utilisateur."""

    def test_returns_logger_instance(self):
        """Doit retourner une instance de Logger."""
        logger = configure_user_logging("test-user-1")
        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self):
        """Le logger doit avoir le nom de l'utilisateur."""
        logger = configure_user_logging("user-abc-123")
        assert logger.name == "user-abc-123"

    def test_logger_has_correct_level(self):
        """Le logger doit avoir le niveau spécifié."""
        logger = configure_user_logging("test-level", level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_creates_log_directory(self):
        """Doit créer le répertoire Logs s'il n'existe pas."""
        configure_user_logging("test-dir-creation")
        assert os.path.exists("Logs")

    def test_creates_log_file(self):
        """Doit créer un fichier log pour l'utilisateur."""
        configure_user_logging("test-file-creation")
        assert os.path.exists("Logs/test-file-creation.log")

    def test_does_not_duplicate_handlers(self):
        """Ne doit pas dupliquer les handlers si appelé plusieurs fois."""
        logger1 = configure_user_logging("test-no-dup")
        handler_count_1 = len(logger1.handlers)

        logger2 = configure_user_logging("test-no-dup")
        handler_count_2 = len(logger2.handlers)

        assert handler_count_1 == handler_count_2

    def test_logger_can_write(self, tmp_path):
        """Le logger doit pouvoir écrire des messages."""
        logger = configure_user_logging("test-write")
        logger.info("Test message")
        # Vérifier que le fichier log contient le message
        log_file = os.path.join("Logs", "test-write.log")
        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            content = f.read()
            assert "Test message" in content
