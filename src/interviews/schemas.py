from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional


class InterviewsBase(BaseModel):
    id: Optional[UUID4]
    user_id: Optional[UUID4]
    company_profile_id: Optional[UUID4]
    job_position: str
    interviewr_name: str
    online_link: str
    date: datetime
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
    

class InterviewsCreate(InterviewsBase):
    pass


class InterviewsUpdate(InterviewsBase):
    pass

