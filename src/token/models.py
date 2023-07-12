# Python
import datetime
from uuid import uuid4

from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    access_token = Column(String(), index=True)
    refresh_token = Column(String(), index=True)
    confirmation_code = Column(String(), index=True)
    expiration_date_code = Column(String(), index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
