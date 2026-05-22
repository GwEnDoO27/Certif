"""
Tests unitaires pour api/utils/convert.py
Couvre : code_comptas, code_comptas_gen_aux, code_journal,
         extract_bill_values, get_document_type, merged_csv
"""

import os
import csv
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from schemas.model import User, UserCodeMap, UserCodeGenAux, UserJournal
from utils.convert import (
    code_comptas,
    code_comptas_gen_aux,
    code_journal,
    extract_bill_values,
    get_document_type,
    merged_csv,
)


class TestCodeComptas:
    """Tests pour la mise à jour des codes comptables."""

    def test_update_existing_code_map(self, db_session, sample_user_with_codes, mock_logger):
        """Doit mettre à jour une map existante."""
        new_data = {"001 SURGELE": "999999"}
        result = code_comptas(db_session, sample_user_with_codes.id, new_data, mock_logger)
        assert result["001 SURGELE"] == "999999"
        # Les autres valeurs doivent être conservées
        assert result["002 ALIMENTAIRE"] == "601100"

    def test_create_new_code_map_with_defaults(self, db_session, mock_logger):
        """Doit créer une nouvelle map avec les défauts si aucune n'existe."""
        user = User(id=100, uid="new-code-user")
        db_session.add(user)
        db_session.commit()

        new_data = {"CUSTOM_KEY": "123456"}
        result = code_comptas(db_session, user.id, new_data, mock_logger)

        assert result is not None
        assert "001 SURGELE" in result  # défaut
        assert "CUSTOM_KEY" in result   # ajouté
        assert result["CUSTOM_KEY"] == "123456"

    def test_ignores_empty_values(self, db_session, sample_user_with_codes, mock_logger):
        """Ne doit pas ajouter les valeurs vides ou whitespace."""
        new_data = {"EMPTY_KEY": "", "SPACE_KEY": "   "}
        result = code_comptas(db_session, sample_user_with_codes.id, new_data, mock_logger)
        assert "EMPTY_KEY" not in result
        assert "SPACE_KEY" not in result

    def test_logs_error_on_failure(self, mock_logger):
        """Doit logger l'erreur en cas de problème."""
        # Passer une session mock qui lève une exception
        from unittest.mock import MagicMock
        bad_session = MagicMock()
        bad_session.query.side_effect = Exception("DB connection error")
        with pytest.raises(Exception, match="DB connection error"):
            code_comptas(bad_session, 9999, {"key": "val"}, mock_logger)
        mock_logger.error.assert_called()


class TestCodeComptasGenAux:
    """Tests pour la mise à jour des codes généraux/auxiliaires."""

    def test_update_existing_gen_aux_map(self, db_session, sample_user_with_codes, mock_logger):
        """Doit mettre à jour les codes gen/aux existants."""
        new_data = {"Code General 401000": "999000"}
        result = code_comptas_gen_aux(db_session, sample_user_with_codes.id, new_data, mock_logger)
        assert result["Code General 401000"] == "999000"

    def test_create_new_gen_aux_with_defaults(self, db_session, mock_logger):
        """Doit créer une map gen/aux avec les défauts."""
        user = User(id=101, uid="new-genaux-user")
        db_session.add(user)
        db_session.commit()

        result = code_comptas_gen_aux(db_session, user.id, {"NEW": "value"}, mock_logger)
        assert "Code General 401000" in result  # défaut
        assert "NEW" in result

    def test_ignores_empty_values(self, db_session, sample_user_with_codes, mock_logger):
        """Ne doit pas ajouter les valeurs vides."""
        result = code_comptas_gen_aux(
            db_session, sample_user_with_codes.id, {"EMPTY": ""}, mock_logger
        )
        assert "EMPTY" not in result


class TestCodeJournal:
    """Tests pour la mise à jour du code journal."""

    def test_update_existing_journal(self, db_session, sample_user_with_codes, mock_logger):
        """Doit mettre à jour le journal existant."""
        new_data = {"Journal": "VNT"}
        result = code_journal(db_session, sample_user_with_codes.id, new_data, mock_logger)
        assert result["Journal"] == "VNT"

    def test_create_new_journal_with_defaults(self, db_session, mock_logger):
        """Doit créer un journal avec le défaut ACM."""
        user = User(id=102, uid="new-journal-user")
        db_session.add(user)
        db_session.commit()

        result = code_journal(db_session, user.id, {"Extra": "XYZ"}, mock_logger)
        assert result["Journal"] == "ACM"  # défaut
        assert result["Extra"] == "XYZ"

    def test_ignores_empty_values(self, db_session, sample_user_with_codes, mock_logger):
        """Ne doit pas ajouter les valeurs vides."""
        result = code_journal(
            db_session, sample_user_with_codes.id, {"EMPTY": ""}, mock_logger
        )
        assert "EMPTY" not in result

    def test_merge_preserves_existing_keys(self, db_session, sample_user_with_codes, mock_logger):
        """Doit préserver les clés existantes lors de la fusion."""
        # D'abord ajouter une clé
        code_journal(db_session, sample_user_with_codes.id, {"Key1": "Val1"}, mock_logger)
        # Puis ajouter une autre clé
        result = code_journal(db_session, sample_user_with_codes.id, {"Key2": "Val2"}, mock_logger)
        assert result["Key1"] == "Val1"
        assert result["Key2"] == "Val2"


class TestGetDocumentType:
    """Tests pour la détection du type de document EDI."""

    def test_detect_facture(self, tmp_path, mock_logger):
        """Doit détecter une Facture (BGM+380)."""
        file_path = tmp_path / "facture.txt"
        file_path.write_text("UNH+1+INVOIC\nBGM+380+REF001+9'\n", encoding="ISO-8859-1")
        result = get_document_type(str(file_path), mock_logger)
        assert result == "Facture"

    def test_detect_avoir(self, tmp_path, mock_logger):
        """Doit détecter un Avoir (BGM+381)."""
        file_path = tmp_path / "avoir.txt"
        file_path.write_text("UNH+1+INVOIC\nBGM+381+REF002+9'\n", encoding="ISO-8859-1")
        result = get_document_type(str(file_path), mock_logger)
        assert result == "Avoir"

    def test_default_to_facture_when_no_bgm(self, tmp_path, mock_logger):
        """Doit retourner Facture par défaut si pas de BGM."""
        file_path = tmp_path / "unknown.txt"
        file_path.write_text("UNH+1+INVOIC\nNAD+BY+1234'\n", encoding="ISO-8859-1")
        result = get_document_type(str(file_path), mock_logger)
        assert result == "Facture"

    def test_handles_file_not_found(self, mock_logger):
        """Doit gérer un fichier inexistant sans crash."""
        result = get_document_type("/nonexistent/file.txt", mock_logger)
        assert result == "Facture"
        mock_logger.warning.assert_called()


class TestExtractBillValues:
    """Tests pour l'extraction des valeurs depuis un fichier EDI."""

    def test_extracts_reference(self, sample_edi_file, db_session, sample_user_with_codes, mock_logger):
        """Doit extraire la référence BGM."""
        result = extract_bill_values(
            sample_edi_file, db_session, sample_user_with_codes.uid, mock_logger
        )
        assert result["reference"] == "INV-2023-001"

    def test_extracts_date(self, sample_edi_file, db_session, sample_user_with_codes, mock_logger):
        """Doit extraire et formater la date DTM 137."""
        result = extract_bill_values(
            sample_edi_file, db_session, sample_user_with_codes.uid, mock_logger
        )
        assert result["date"] == "15/06/2023"

    def test_extracts_article_values(self, sample_edi_file, db_session, sample_user_with_codes, mock_logger):
        """Doit extraire les valeurs des articles (MOA)."""
        result = extract_bill_values(
            sample_edi_file, db_session, sample_user_with_codes.uid, mock_logger
        )
        assert len(result["articles_values"]) == 2
        assert "150.00" in result["articles_values"]
        assert "250.00" in result["articles_values"]

    def test_extracts_tva(self, sample_edi_file, db_session, sample_user_with_codes, mock_logger):
        """Doit extraire le montant TVA."""
        result = extract_bill_values(
            sample_edi_file, db_session, sample_user_with_codes.uid, mock_logger
        )
        assert result["tva"] == 80.0

    def test_extracts_net_payable(self, sample_edi_file, db_session, sample_user_with_codes, mock_logger):
        """Doit extraire le net à payer."""
        result = extract_bill_values(
            sample_edi_file, db_session, sample_user_with_codes.uid, mock_logger
        )
        assert result["net_payable"] == 400.0

    def test_raises_on_non_edi_file(self, tmp_path, db_session, sample_user_with_codes, mock_logger):
        """Doit lever une erreur si le fichier n'est pas un fichier valide."""
        file_path = tmp_path / "not_edi.txt"
        file_path.write_text("Ceci est un fichier texte normal sans format attendu", encoding="ISO-8859-1")
        with pytest.raises(ValueError, match="Fichier non-EDI"):
            extract_bill_values(
                str(file_path), db_session, sample_user_with_codes.uid, mock_logger
            )

    def test_raises_on_nonexistent_file(self, db_session, sample_user_with_codes, mock_logger):
        """Doit lever une erreur si le fichier n'existe pas."""
        with pytest.raises(Exception):
            extract_bill_values(
                "/nonexistent/file.txt", db_session, sample_user_with_codes.uid, mock_logger
            )


class TestMergedCsv:
    """Tests pour la fusion de fichiers CSV."""

    def test_merges_multiple_csvs(self, tmp_path, mock_logger):
        """Doit fusionner plusieurs CSV en un seul."""
        store_dir = tmp_path / "MAGASIN1"
        store_dir.mkdir()

        # Créer 2 fichiers CSV
        for i in range(2):
            csv_path = store_dir / f"file_{i}.csv"
            df = pd.DataFrame({"COL_A": [f"val_{i}"], "COL_B": [i * 100]})
            df.to_csv(csv_path, index=False)

        merged_csv("MAGASIN1", str(tmp_path), mock_logger)

        output = tmp_path / "MAGASIN1.csv"
        assert output.exists()

        result_df = pd.read_csv(output)
        assert len(result_df) == 2

    def test_handles_empty_directory(self, tmp_path, mock_logger):
        """Doit gérer un répertoire vide sans crash."""
        store_dir = tmp_path / "EMPTY_STORE"
        store_dir.mkdir()

        merged_csv("EMPTY_STORE", str(tmp_path), mock_logger)
        mock_logger.warning.assert_called()

    def test_handles_nonexistent_directory(self, tmp_path, mock_logger):
        """Doit gérer un répertoire inexistant sans crash."""
        merged_csv("NONEXISTENT", str(tmp_path), mock_logger)
        mock_logger.warning.assert_called()
