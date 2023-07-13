# Python
from email import policy
from typing import Optional, Union, List, Any
import random
from datetime import timedelta, datetime

# Pydantic
from pydantic import BaseModel, EmailStr, UUID4, Field

# app utilities



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


# class TokenCreate:
#     @staticmethod
#     def generate_code(name: str, minutes: int, user_id: UUID4) -> int:
#         token = Token.get_token_by_user(user_id=user_id)

#         if token:
#             TokenCreate.delete_code(token_id=token.id)

#         new_token = TokenBase()
#         new_token.name = name
#         new_token.code = random.randint(100000, 999999)
#         new_token.expiration = datetime.utcnow() + timedelta(minutes=minutes)

#         Token.create_token(user_id=user_id, name=new_token.name, code=new_token.code, expiration=new_token.expiration)

#         return new_token.code
    
        
    