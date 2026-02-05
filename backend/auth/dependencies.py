"""
Token verification dependency for the authentication backend.
Provides dependency injection for JWT token validation.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import jwt
from pydantic import ValidationError
from backend.config.database import settings
from backend.schemas.user import TokenData
from backend.auth.utils import decode_access_token


security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get the current user from the JWT token.

    Args:
        token: The HTTP authorization credentials containing the JWT token

    Returns:
        TokenData: The token data containing user information

    Raises:
        HTTPException: If the token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token.credentials, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_identifier: str = payload.get("sub")
        if user_identifier is None:
            raise credentials_exception

        # The 'sub' field contains the user ID, not email, so we pass it as email field temporarily
        # The /me endpoint will handle looking up by ID instead of email
        token_data = TokenData(email=user_identifier)
    except (jwt.JWTError, ValidationError):
        raise credentials_exception

    return token_data


async def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT token and return the token data if valid.

    Args:
        token: The JWT token to verify

    Returns:
        Optional[TokenData]: The token data if the token is valid, None otherwise
    """
    try:
        decoded_token = decode_access_token(token)
        if decoded_token and "sub" in decoded_token:
            return TokenData(email=decoded_token["sub"])
        return None
    except Exception:
        return None