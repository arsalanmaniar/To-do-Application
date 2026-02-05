"""
Authentication API routes for the backend.
Handles user registration, login, and JWT token generation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
import re

from backend.config.database import get_db
from app.models.user import User
from backend.schemas.user import UserCreate, UserResponse, Token, UserLogin
from backend.auth.utils import get_password_hash, verify_password, create_access_token
from backend.auth.dependencies import get_current_user


router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.

    Args:
        user_data: User registration data containing email and password
        db: Database session dependency

    Returns:
        UserResponse: Created user data without password
    """
    # Validate email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    from uuid import uuid4
    db_user = User(
        id=str(uuid4()),  # Generate a UUID for the user ID
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at
    )


@router.post("/sign-up", response_model=UserResponse)
def sign_up(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with email and password (alias for register).

    Args:
        user_data: User registration data containing email and password
        db: Database session dependency

    Returns:
        UserResponse: Created user data without password
    """
    # Validate email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    from uuid import uuid4
    db_user = User(
        id=str(uuid4()),  # Generate a UUID for the user ID
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at
    )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.

    Args:
        credentials: User credentials containing email and password
        db: Database session dependency

    Returns:
        Token: JWT access token and token type
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token - use user ID instead of email for database relationships
    access_token_expires = timedelta(minutes=30)  # Use configurable value
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.seconds
    )


@router.post("/sign-in", response_model=Token)
def sign_in(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token (alias for login).

    Args:
        credentials: User credentials containing email and password
        db: Database session dependency

    Returns:
        Token: JWT access token and token type
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token - use user ID instead of email for database relationships
    access_token_expires = timedelta(minutes=30)  # Use configurable value
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.seconds
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the current user's profile information.

    Args:
        current_user: The authenticated user obtained from the JWT token
        db: Database session dependency

    Returns:
        UserResponse: Current user's profile data
    """
    # Find the user in the database by ID (since current_user.email contains the user ID from token)
    user = db.query(User).filter(User.id == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.get("/protected-test")
def protected_test_endpoint(current_user: User = Depends(get_current_user)):
    """
    Example of a protected endpoint that requires JWT token validation.

    Args:
        current_user: The authenticated user obtained from the JWT token

    Returns:
        dict: Confirmation that the user has access to the protected endpoint
    """
    return {
        "message": "Access granted to protected endpoint",
        "user_email": current_user.email,
        "detail": "This endpoint is protected and requires a valid JWT token"
    }