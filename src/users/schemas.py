# Python
from email import policy
from typing import Optional, Union, List, Any
from datetime import datetime

# Pydantic
from pydantic import BaseModel, EmailStr, UUID4, Field

# app utilities
from src.roles.schemas import Role, UserRole

# Shared properties
# class UserBase(BaseModel):
#     email: Optional[EmailStr] = None
#     is_active: Optional[bool] = False
#     full_name: Optional[str] = None
#     is_blocked: bool | None = False

#     class Config:
#         orm_mode = True

#-----------------------------

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False
    password: Optional[str]

    class Config:
        orm_mode = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str] = None
    
   
    email: EmailStr
    password: Union[str, None]
    code: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID4
    roles: Optional[List[Role]]  
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

class Msg(BaseModel):
    msg: str