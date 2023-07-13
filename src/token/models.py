# Python
from datetime import datetime, timedelta
from uuid import uuid4
import random

from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base


user_tokens = Table(
    "user_tokens",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("token_id", ForeignKey("tokens.id"), primary_key=True, nullable=False),
)


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    name = Column(String(), index=True)
    code = Column(Integer(), index=True)
    expiration = Column(DateTime())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    users = relationship("User", secondary=user_tokens, back_populates="tokens")
    created_at = Column(DateTime(), default=datetime.utcnow)
        
        
