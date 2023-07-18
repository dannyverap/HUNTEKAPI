from pydantic import BaseModel, UUID4
from typing import List, Optional
from src.job_offers.schemas import JobOffersBase
from src.user_profile.schemas import UserProfileBase

class JobApplicationBase(BaseModel):
    id: Optional[UUID4]
    job_offer_id: UUID4
    user_profile_id: UUID4
    status: str = "pending"

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(JobApplicationBase):
    pass

class JobApplicationInDB(JobApplicationBase):
    id: UUID4

class JobApplicationResponse(JobApplicationInDB):
    job_offer: JobOffersBase
    user_profile: UserProfileBase

