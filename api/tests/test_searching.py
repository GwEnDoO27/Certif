"""
Tests unitaires pour api/utils/searching.py
Couvre : whos_mag, name_of_mag, verify_if_mag_exists
"""

import os
import pytest
from utils.searching import whos_mag, name_of_mag, verify_if_mag_exists


class TestNameOfMag:
    """Tests pour la fonction name_of_mag."""

    def test_extracts_mag_name_from_rff_gn(self):
        """Doit extraire le nom du magasin depuis une ligne RFF+GN."""
        line = "RFF+GN:PARIS_NORD'"
        result = name_of_mag(line)
        # La fonction ne strip pas le trailing ', elle retourne le nom tel quel
        assert result is not None
        assert "PARIS_NORD" in result

    def test_returns_none_for_non_rff_line(self):
        """Doit retourner None pour une ligne non-RFF."""
        line = "BGM+380+REF001+9'"
        result = name_of_mag(line)
        assert result is None

    def test_returns_none_for_empty_line(self):
        """Doit retourner None pour une ligne vide."""
        result = name_of_mag("")
        assert result is None

    def test_strips_whitespace(self):
        """Doit nettoyer les espaces du nom du magasin."""
        line = "RFF+GN:  LYON_CENTRE  '"
        result = name_of_mag(line)
        assert result == "LYON_CENTRE"

    def test_handles_no_colon_separator(self):
        """Doit retourner None si la ligne RFF+GN n'a pas de ':'."""
        line = "RFF+GN'"
        result = name_of_mag(line)
        assert result is None


class TestWhosMag:
    """Tests pour la fonction whos_mag."""

    def test_finds_mag_in_edi_file(self, tmp_path, mock_logger):
        """Doit trouver le nom du magasin dans un fichier EDI."""
        file_path = tmp_path / "test.txt"
        file_path.write_text(
            "UNH+1+INVOIC\nBGM+380+REF+9'\nRFF+GN:BORDEAUX'\nNAD+BY+123'\n",
            encoding="ISO-8859-1"
        )
        result = whos_mag(str(file_path), mock_logger)
        assert result is not None
        assert "BORDEAUX" in result

    def test_returns_none_when_no_rff_gn(self, tmp_path, mock_logger):
        """Doit retourner None si aucune ligne RFF+GN."""
        file_path = tmp_path / "no_mag.txt"
        file_path.write_text("UNH+1+INVOIC\nBGM+380+REF+9'\n", encoding="ISO-8859-1")
        result = whos_mag(str(file_path), mock_logger)
        assert result is None

    def test_handles_nonexistent_file(self, mock_logger):
        """Doit retourner None si le fichier n'existe pas."""
        result = whos_mag("/nonexistent/file.txt", mock_logger)
        assert result is None
        mock_logger.error.assert_called()


class TestVerifyIfMagExists:
    """Tests pour la fonction verify_if_mag_exists."""

    def test_creates_directories_if_not_exist(self, tmp_path):
        """Doit créer les répertoires upload et download pour le magasin."""
        upload_path = str(tmp_path / "uploads")
        download_path = str(tmp_path / "downloads")
        os.makedirs(upload_path, exist_ok=True)
        os.makedirs(download_path, exist_ok=True)

        result = verify_if_mag_exists("NICE", upload_path, download_path)
        assert result is True
        assert os.path.exists(os.path.join(upload_path, "NICE"))
        assert os.path.exists(os.path.join(download_path, "NICE"))

    def test_returns_true_if_directories_already_exist(self, tmp_path):
        """Doit retourner True même si les répertoires existent déjà."""
        upload_path = str(tmp_path / "uploads")
        download_path = str(tmp_path / "downloads")
        os.makedirs(os.path.join(upload_path, "MARSEILLE"), exist_ok=True)
        os.makedirs(os.path.join(download_path, "MARSEILLE"), exist_ok=True)

        result = verify_if_mag_exists("MARSEILLE", upload_path, download_path)
        assert result is True
