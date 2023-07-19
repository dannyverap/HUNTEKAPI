from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
import datetime

class Interviews(Base):
    __tablename__ = "interviews"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"))
    interview_type = Column(String)
    interview_name = Column(String)
    online_link = Column(String)
    date = Column(DateTime)
    notes = Column(Text)

    user_profile = relationship("UserProfile", back_populates="interviews")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )

