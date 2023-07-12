from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class BusinessProfileBase(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
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

class BusinessProfileCreate(BusinessProfileBase):
    profile_picture: str
    applications: List[str]
    interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime
    
    
class UserProfileUpdate(BusinessProfileBase):
    pass
