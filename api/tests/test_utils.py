"""
Tests unitaires pour api/utils/utils.py
Couvre : query_code_comptas, query_code_gen_aux, query_journal_code, NewUser
"""

import pytest
from schemas.model import User, UserCodeMap, UserCodeGenAux, UserJournal
from utils.utils import query_code_comptas, query_code_gen_aux, query_journal_code, NewUser


class TestQueryCodeComptas:
    """Tests pour la fonction query_code_comptas."""

    def test_returns_code_map_for_existing_user(self, db_session, sample_user_with_codes, mock_logger):
        """Doit retourner la map des codes comptables pour un utilisateur existant."""
        result = query_code_comptas(db_session, sample_user_with_codes.uid, mock_logger)
        assert result is not None
        assert isinstance(result, dict)
        assert "001 SURGELE" in result
        assert result["001 SURGELE"] == "601100"

    def test_returns_none_for_nonexistent_user(self, db_session, mock_logger):
        """Doit retourner None si l'utilisateur n'existe pas."""
        result = query_code_comptas(db_session, "nonexistent-uid", mock_logger)
        assert result is None

    def test_returns_none_when_no_code_map(self, db_session, sample_user, mock_logger):
        """Doit retourner None si l'utilisateur n'a pas de code map."""
        result = query_code_comptas(db_session, sample_user.uid, mock_logger)
        assert result is None

    def test_logs_info_when_user_not_found(self, db_session, mock_logger):
        """Doit logger un message info quand l'utilisateur n'est pas trouvé."""
        query_code_comptas(db_session, "unknown-uid", mock_logger)
        mock_logger.info.assert_called()


class TestQueryCodeGenAux:
    """Tests pour la fonction query_code_gen_aux."""

    def test_returns_gen_aux_map_for_existing_user(self, db_session, sample_user_with_codes, mock_logger):
        """Doit retourner la map des codes gen/aux pour un utilisateur existant."""
        result = query_code_gen_aux(db_session, sample_user_with_codes.uid, mock_logger)
        assert result is not None
        assert isinstance(result, dict)
        assert "Code General 401000" in result
        assert result["Code General 401000"] == "401000"

    def test_returns_none_for_nonexistent_user(self, db_session, mock_logger):
        """Doit retourner None si l'utilisateur n'existe pas."""
        result = query_code_gen_aux(db_session, "nonexistent-uid", mock_logger)
        assert result is None

    def test_returns_none_when_no_gen_aux_map(self, db_session, sample_user, mock_logger):
        """Doit retourner None si l'utilisateur n'a pas de map gen/aux."""
        result = query_code_gen_aux(db_session, sample_user.uid, mock_logger)
        assert result is None


class TestQueryJournalCode:
    """Tests pour la fonction query_journal_code."""

    def test_returns_journal_map_for_existing_user(self, db_session, sample_user_with_codes, mock_logger):
        """Doit retourner la map journal pour un utilisateur existant."""
        result = query_journal_code(db_session, sample_user_with_codes.uid, mock_logger)
        assert result is not None
        assert isinstance(result, dict)
        assert "Journal" in result
        assert result["Journal"] == "ACM"

    def test_returns_none_for_nonexistent_user(self, db_session, mock_logger):
        """Doit retourner None si l'utilisateur n'existe pas."""
        result = query_journal_code(db_session, "nonexistent-uid", mock_logger)
        assert result is None

    def test_returns_none_when_no_journal(self, db_session, sample_user, mock_logger):
        """Doit retourner None si l'utilisateur n'a pas de journal."""
        result = query_journal_code(db_session, sample_user.uid, mock_logger)
        assert result is None


class TestNewUser:
    """Tests pour la fonction NewUser (provisionnement automatique)."""

    def test_creates_code_maps_for_new_user(self, db_session):
        """Doit créer les code maps pour un utilisateur sans maps."""
        # Créer un utilisateur sans codes
        user = User(id=10, uid="new-user-uid")
        db_session.add(user)
        db_session.commit()

        result = NewUser(db_session)

        # Vérifier que les code maps ont été créées
        code_map = db_session.query(UserCodeMap).filter_by(user_id=10).first()
        gen_aux = db_session.query(UserCodeGenAux).filter_by(user_id=10).first()
        journal = db_session.query(UserJournal).filter_by(user_id=10).first()

        assert code_map is not None
        assert gen_aux is not None
        assert journal is not None
        assert "001 SURGELE" in code_map.code_map
        assert "Code General 401000" in gen_aux.code_map_gen_aux
        assert "Journal" in journal.journal_map

    def test_does_not_duplicate_existing_maps(self, db_session, sample_user_with_codes):
        """Ne doit pas recréer les maps si elles existent déjà."""
        initial_count = db_session.query(UserCodeMap).filter_by(
            user_id=sample_user_with_codes.id
        ).count()

        NewUser(db_session)

        final_count = db_session.query(UserCodeMap).filter_by(
            user_id=sample_user_with_codes.id
        ).count()

        assert initial_count == final_count

    def test_handles_empty_database(self, db_session):
        """Doit gérer le cas où il n'y a aucun utilisateur."""
        # Supprimer tous les utilisateurs
        db_session.query(UserCodeMap).delete()
        db_session.query(UserCodeGenAux).delete()
        db_session.query(UserJournal).delete()
        db_session.query(User).delete()
        db_session.commit()

        result = NewUser(db_session)
        assert result is not None

    def test_default_code_map_values(self, db_session):
        """Vérifie que les valeurs par défaut des codes sont correctes."""
        user = User(id=20, uid="default-values-user")
        db_session.add(user)
        db_session.commit()

        NewUser(db_session)

        code_map = db_session.query(UserCodeMap).filter_by(user_id=20).first()
        assert code_map.code_map["001 SURGELE"] == "601100"
        assert code_map.code_map["003 EMBALLAGE"] == "602201"
        assert code_map.code_map["00X DIVERS"] == "471000"

        gen_aux = db_session.query(UserCodeGenAux).filter_by(user_id=20).first()
        assert gen_aux.code_map_gen_aux["Code Auxilliaire 401000"] == "401LR"

        journal = db_session.query(UserJournal).filter_by(user_id=20).first()
        assert journal.journal_map["Journal"] == "ACM"
