from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class JobOffersBase(BaseModel):
    id: Optional[UUID4]
    job_title: str
    description: str
    modality: str
    work_schedule: str
    requirements: str
    postulants: Optional[List[str]]
    user_id: Optional[UUID4]
    company_profile_id: Optional[UUID4]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class JobOffersCreate(JobOffersBase):
    pass


class JobOffersUpdate(JobOffersBase):
    pass
