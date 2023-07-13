from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.base import Base
from src.users.models import User
import datetime


class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)

    company_logo = Column(String)
    company_description = Column(Text)
    company_why_us = Column(Text)
    company_know_us_better_video = Column(Text) 
    job_offers = Column(ARRAY(String)) ## debería ser el mismo modelo que applications de user_profile
    interviews = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="company_profile", uselist=False)
    