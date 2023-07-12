from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.base import Base
from src.users.models import User
import datetime


class CompanyProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    business_logo = Column(String)
    business_description = Column(Text)
    business_why_us = Column(Text)
    business_know_us_better_video = Column(Text) 
    job_offers = Column(ARRAY(String)) ## debería ser el mismo modelo que applications de user_profile
    interviews = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )
    user = relationship("User", back_populates="user_profile", uselist=False) ##! revisar
