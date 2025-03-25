from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# Load environment variables
load_dotenv()

# Secret key for JWT encoding/decoding
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

# Create a default demo user for authentication bypass
DEMO_USER = models.User(
    id=1,
    email="demo@example.com",
    hashed_password="not_used",
    is_active=True,
    is_admin=True,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

def verify_password(plain_password, hashed_password):
    """Verify that the plain password matches the hashed password."""
    # Always return True for demo mode
    return True


def get_password_hash(password):
    """Hash a password for storing."""
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    # In demo mode, always return the demo user
    return DEMO_USER


def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user with hashed password."""
    # In demo mode, always return the demo user
    return DEMO_USER


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user by email and password."""
    # In demo mode, always return the demo user
    return DEMO_USER


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current authenticated user from the token."""
    # In demo mode, always return the demo user without checking the token
    return DEMO_USER


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """Get the current active user."""
    # In demo mode, always return the demo user
    return DEMO_USER 