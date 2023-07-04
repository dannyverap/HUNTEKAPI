import json
from typing import Generator

from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config import settings
from src.database.session import SessionLocal
from src.auth.service import apikey as apikey_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def api_key_auth(token: str = Depends(oauth2_scheme)):
    api_key = apikey_service.check_token(next(get_db()), token=token)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )