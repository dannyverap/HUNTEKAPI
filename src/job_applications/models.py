from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, Text, ARRAY, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.base import Base
import datetime

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)

    job_offer_id = Column(UUID(as_uuid=True), ForeignKey("job_offers.id"), index=True)
    job_offer= relationship("JobOffer", back_populates="job_offer_applications")

    user_profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), index=True)
    user_profile     = relationship("UserProfile", back_populates="applications")

    status = Column(Enum("pending", "under_review", "shortlisted", "interview_scheduled", "interview_completed", "reference_check", "offer_extended", "offer_accepted", "rejected", "withdrawn", name="job_applications_status"), default="pending")

