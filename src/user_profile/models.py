from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.base import Base
from src.users.models import User
import datetime


class user_profile(Base):
    __tablename__ = "user_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    profile_picture = Column(String)
    applications = Column(ARRAY(String))
    interviews = Column(ARRAY(String))
    responses = Column(Text)
    phone_number = Column(String)
    resume = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow(),
    )
    user = relationship("User", back_populates="user_profile", uselist=False) ##! revisar


    ## En modelo User va :user_profile = relationship("UserProfile", uselist=False, back_populates="user")
