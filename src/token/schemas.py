# Python
from email import policy
from typing import Optional, Union, List, Any
from datetime import datetime

# Pydantic
from pydantic import BaseModel, EmailStr, UUID4, Field

# app utilities
from src.roles.schemas import Role, UserRole


class TokenBase(BaseModel):

    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    confirmation_code: Optional[str] = None
    expiration_date_code: Optional[str] = None

    class Config:
        orm_mode = True

# Properties to receive via API on creation


class TokenCreate(TokenBase):

    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    confirmation_code: Optional[str] = None
    expiration_date_code: Optional[str] = None
