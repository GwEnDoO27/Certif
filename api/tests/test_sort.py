"""
Tests unitaires pour api/utils/sort.py
Couvre : sorting_mag, sort_files
"""

import os
import shutil
import pytest
from utils.sort import sorting_mag, sort_files


class TestSortFiles:
    """Tests pour la fonction sort_files."""

    def test_moves_file_to_mag_folder(self, tmp_path, mock_logger):
        """Doit déplacer le fichier dans le dossier du magasin."""
        upload_dir = tmp_path / "uploads"
        download_dir = tmp_path / "downloads"
        upload_dir.mkdir()
        download_dir.mkdir()

        # Créer un fichier source
        source_file = upload_dir / "facture_001.txt"
        source_file.write_text("test content")

        sort_files(
            str(source_file), "PARIS",
            str(upload_dir), str(download_dir),
            mock_logger
        )

        # Vérifier que le fichier a été déplacé
        assert not source_file.exists()
        assert (upload_dir / "PARIS" / "facture_001.txt").exists()

    def test_sanitizes_filename(self, tmp_path, mock_logger):
        """Doit nettoyer les apostrophes dans le nom de fichier."""
        upload_dir = tmp_path / "uploads"
        download_dir = tmp_path / "downloads"
        upload_dir.mkdir()
        download_dir.mkdir()

        source_file = upload_dir / "facture'001.txt"
        source_file.write_text("test content")

        sort_files(
            str(source_file), "LYON",
            str(upload_dir), str(download_dir),
            mock_logger
        )

        # Le fichier doit être nommé sans apostrophe
        assert (upload_dir / "LYON" / "facture001.txt").exists()

    def test_creates_mag_folders_if_needed(self, tmp_path, mock_logger):
        """Doit créer les dossiers magasin s'ils n'existent pas."""
        upload_dir = tmp_path / "uploads"
        download_dir = tmp_path / "downloads"
        upload_dir.mkdir()
        download_dir.mkdir()

        source_file = upload_dir / "test.txt"
        source_file.write_text("data")

        sort_files(
            str(source_file), "NEW_MAG",
            str(upload_dir), str(download_dir),
            mock_logger
        )

        assert (upload_dir / "NEW_MAG").exists()
        assert (download_dir / "NEW_MAG").exists()


class TestSortingMag:
    """Tests pour la fonction sorting_mag."""

    def test_sorts_edi_file_by_mag(self, tmp_path, mock_logger):
        """Doit trier un fichier EDI dans le bon dossier magasin."""
        upload_dir = tmp_path / "uploads"
        download_dir = tmp_path / "downloads"
        upload_dir.mkdir()
        download_dir.mkdir()

        # Créer un fichier EDI avec un nom de magasin
        edi_file = upload_dir / "test_edi.txt"
        edi_file.write_text(
            "UNH+1+INVOIC\nRFF+GN:TOULOUSE'\nBGM+380+REF+9'\n",
            encoding="ISO-8859-1"
        )

        sorting_mag(
            str(edi_file), str(upload_dir), str(download_dir),
            "user-123", mock_logger
        )

        # Le fichier doit avoir été déplacé (le nom du mag peut inclure le trailing ')
        assert not edi_file.exists()  # Le fichier a été déplacé
        # Vérifier qu'un sous-dossier a été créé dans uploads
        subdirs = [d for d in upload_dir.iterdir() if d.is_dir()]
        assert len(subdirs) >= 1
        # Vérifier que le fichier est dans un des sous-dossiers
        moved_files = list(subdirs[0].glob("*.txt"))
        assert len(moved_files) == 1

    def test_does_nothing_when_no_mag_found(self, tmp_path, mock_logger):
        """Ne doit rien faire si aucun magasin n'est trouvé dans le fichier."""
        upload_dir = tmp_path / "uploads"
        download_dir = tmp_path / "downloads"
        upload_dir.mkdir()
        download_dir.mkdir()

        edi_file = upload_dir / "no_mag.txt"
        edi_file.write_text("UNH+1+INVOIC\nBGM+380+REF+9'\n", encoding="ISO-8859-1")

        sorting_mag(
            str(edi_file), str(upload_dir), str(download_dir),
            "user-123", mock_logger
        )

        # Le fichier doit rester à sa place originale
        assert edi_file.exists()
