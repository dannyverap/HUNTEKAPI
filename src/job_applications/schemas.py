from pydantic import BaseModel, UUID4
from typing import List, Optional
from src.job_offers.schemas import JobOffersBase
from src.user_profile.schemas import UserProfileBase

class JobApplicationBase(BaseModel):
    id: Optional[UUID4]
    job_offer_id: Optional[UUID4]
    user_profile_id: Optional[UUID4]
    status: str = "pending"

    class Config:
        orm_mode = True


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationUpdate(JobApplicationBase):
    pass


class JobApplicationInDB(JobApplicationBase):
    id: UUID4


# Corregir la relación con UserProfile, utilizando List[UUID]
class JobApplicationResponse(BaseModel):
    id: UUID4
    job_offer: JobOffersBase
    user_profile: UserProfileBase

    class Config:
        orm_mode = True