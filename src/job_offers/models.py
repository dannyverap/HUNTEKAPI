from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.base import Base
import datetime

class JobOffer(Base):
    __tablename__ = "job_offers"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    job_title = Column(String)
    description = Column(Text)
    modality = Column(Text)  # Ejemplo: presencial
    work_schedule = Column(Text)  # Ejemplo: fulltime
    requirements = Column(Text) 
    postulants = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    user =  relationship("User", back_populates="job_offers", foreign_keys=[user_id])
    
    company_profile_id = Column(UUID(as_uuid=True), ForeignKey("company_profiles.id"))
    company_profile = relationship("CompanyProfile", back_populates="job_offers")
