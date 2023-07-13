# Python
from datetime import datetime, timedelta
from uuid import uuid4
import random

from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    name = Column(String(), index=True)
    code = Column(Integer(), index=True)
    expiration = Column(DateTime())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")
    created_at = Column(DateTime(), default=datetime.utcnow)
        