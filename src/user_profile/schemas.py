from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class UserProfileBase(BaseModel):
    id: Optional[UUID4]
    user_id: Optional[UUID4]
    profile_picture: Optional[str]
    applications: Optional[List[str]] = []
    responses: str
    phone_number: str
    resume: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass



