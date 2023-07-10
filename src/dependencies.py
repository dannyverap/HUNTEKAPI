from contextlib import contextmanager
import json
from typing import Generator

from src.database.session import SessionLocal

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from src.users.models import User
from src.auth import schemas as auth_schemas
from src.auth import utils as security
from src.users import service as user_service
from src.config import settings
from src.roles.constants import Role

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token",
    scopes={
        Role.ADMIN["name"]: Role.ADMIN["description"],
        Role.READ["name"]: Role.READ["description"],
        Role.EMAIL["name"]: Role.EMAIL["description"],
        Role.USER["name"]: Role.USER["description"],
    },
)


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@contextmanager
def get_db_typer() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Sub is missing, could not validate credentials ",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user_info = payload.get("user_info", None)
        if user_info is None:
            raise credentials_exception

        token_data = auth_schemas.TokenPayload(**user_info)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.user.get(db, id=token_data.id)

    if not user:
        raise credentials_exception
    if security_scopes.scopes and not token_data.role:
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    if security_scopes.scopes and token_data.role not in security_scopes.scopes:
        raise HTTPException(
            status_code=401,
            detail=f"Not enough permissions for {token_data.role}",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return user


def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=[]),
) -> User:
    if not user_service.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
