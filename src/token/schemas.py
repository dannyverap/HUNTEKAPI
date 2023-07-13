# Python
from email import policy
from typing import Optional, Union, List, Any
import random
from datetime import timedelta, datetime

# Pydantic
from pydantic import BaseModel, EmailStr, UUID4, Field


class TokenBase(BaseModel):
    name: str
    code: int
    expiration: datetime 

    class Config:
        orm_mode = True

# Properties to receive via API on creation

class TokenCreate(TokenBase):
    name: str
    code: int
    expiration: datetime
    user_id: UUID4

