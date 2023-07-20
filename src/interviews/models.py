from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
import datetime

class Interviews(Base):
    __tablename__ = "interviews"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    job_position = Column(String)
    interviewr_name = Column(String)
    online_link = Column(String)
    date = Column(DateTime)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    users = relationship("User", back_populates="interviews")
    
    company_profile_id = Column(UUID(as_uuid=True), ForeignKey("company_profiles.id"))
    company_profile = relationship("CompanyProfile", back_populates="interviews")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )

