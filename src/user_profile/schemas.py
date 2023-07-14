from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    profile_picture: Optional[str]
    applications: List[str]
    # interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserProfileCreate(UserProfileBase):
    profile_picture: Optional[str]
    applications: List[str]
    # interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime
    
    
class UserProfileUpdate(UserProfileBase):
    pass





