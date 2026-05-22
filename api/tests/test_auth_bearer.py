"""
Tests unitaires pour api/auth/auth_bearer.py
Couvre : decode_jwt, JWTBearer.verify_jwt
"""

import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from auth.auth_bearer import decode_jwt, JWTBearer, JWT_SECRET_KEY, ALGORITHM


class TestDecodeJwt:
    """Tests pour la fonction decode_jwt."""

    def test_decodes_valid_token(self):
        """Doit décoder un token JWT valide."""
        payload = {"sub": "user123", "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        result = decode_jwt(token)
        assert result["sub"] == "user123"

    def test_raises_on_expired_token(self):
        """Doit lever HTTPException pour un token expiré."""
        payload = {"sub": "user123", "exp": datetime.utcnow() - timedelta(hours=1)}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            decode_jwt(token)
        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    def test_raises_on_invalid_token(self):
        """Doit lever HTTPException pour un token invalide."""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            decode_jwt("invalid.token.string")
        assert exc_info.value.status_code == 401

    def test_raises_on_wrong_secret(self):
        """Doit lever HTTPException si le secret est incorrect."""
        payload = {"sub": "user123", "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(payload, "wrong-secret-key", algorithm=ALGORITHM)
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            decode_jwt(token)

    def test_decodes_token_with_custom_claims(self):
        """Doit décoder un token avec des claims personnalisés."""
        payload = {
            "sub": "user456",
            "role": "admin",
            "email": "admin@test.com",
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        result = decode_jwt(token)
        assert result["role"] == "admin"
        assert result["email"] == "admin@test.com"


class TestJWTBearer:
    """Tests pour la classe JWTBearer."""

    def test_verify_jwt_valid_token(self):
        """Doit retourner True pour un token valide."""
        bearer = JWTBearer()
        payload = {"sub": "user123", "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        assert bearer.verify_jwt(token) is True

    def test_verify_jwt_expired_token(self):
        """Doit retourner False pour un token expiré."""
        bearer = JWTBearer()
        payload = {"sub": "user123", "exp": datetime.utcnow() - timedelta(hours=1)}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        assert bearer.verify_jwt(token) is False

    def test_verify_jwt_invalid_token(self):
        """Doit retourner False pour un token invalide."""
        bearer = JWTBearer()
        assert bearer.verify_jwt("not-a-valid-jwt") is False

    def test_verify_jwt_empty_string(self):
        """Doit retourner False pour une chaîne vide."""
        bearer = JWTBearer()
        assert bearer.verify_jwt("") is False
