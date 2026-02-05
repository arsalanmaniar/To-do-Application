from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.core.config import settings


def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.algorithm]
        )

        # Extract user ID from the payload
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def extract_user_id_from_token(token: str) -> str:
    """
    Extract user ID from JWT token
    """
    payload = verify_jwt_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id