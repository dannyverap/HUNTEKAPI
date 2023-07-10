from pydantic import BaseModel, UUID4
from typing import List
from datetime import datetime


class UserProfileCreate(BaseModel):
    profile_picture: str
    applications: List[str]
    interviews: List[str]
    responses: str
    phone_number: str
    resume: str


class UserProfileUpdate(BaseModel):
    profile_picture: str = None
    applications: List[str] = []
    interviews: List[str] = []
    responses: str = None
    phone_number: str = None
    resume: str = None


class UserProfile(BaseModel):
    id: UUID4
    user_id: UUID4
    profile_picture: str
    applications: List[str]
    interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
