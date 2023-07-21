from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class CompanyProfileBase(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    company_logo: str
    company_description: str
    company_why_us: str
    company_know_us_better_video: str
    job_offers: Optional[List[str]]
    interviews: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CompanyProfileCreate(CompanyProfileBase):
    pass


class CompanyProfileUpdate(CompanyProfileBase):
    pass
