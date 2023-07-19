from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class InterviewsBase(BaseModel):
    profile_id: Optional[UUID]
    interview_type: str
    interview_name: str
    online_link: str
    date: datetime
    notes: str


class InterviewsCreate(InterviewsBase):
    pass


class InterviewsUpdate(InterviewsBase):
    pass


class Interviews(InterviewsBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

