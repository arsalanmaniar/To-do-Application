from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.core.security import extract_user_id_from_token
from app.database.session import get_session
from sqlmodel import Session


def get_current_user_id(authorization: str = Header(...)) -> str:
    """
    Get the current user ID from the JWT token in the Authorization header
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]  # Extract token after "Bearer "
    user_id = extract_user_id_from_token(token)
    return user_id


def get_current_user_id_matching_path(path_user_id: str, current_user_id: str = Depends(get_current_user_id)):
    """
    Verify that the user ID in the JWT token matches the user ID in the path
    """
    if path_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch",
        )

    return current_user_id


def get_db_session():
    """
    Get database session dependency
    """
    yield from get_session()