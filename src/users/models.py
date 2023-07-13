# Python
import datetime
from uuid import uuid4

from sqlalchemy import Table, Boolean, Column, String, DateTime, ForeignKey, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.roles.models import user_roles
from src.token.models import Token


# class User(Base):
#     __tablename__ = "users"
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
#     full_name = Column(String, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=True, default=None)
#     is_active = Column(Boolean(), default=False)
#     roles = relationship("Role", secondary=user_roles, back_populates="users", uselist=False, lazy="joined")
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(
#         DateTime,
#         default=datetime.datetime.utcnow,
#         onupdate=datetime.datetime.utcnow,
#     )

# ----------------------------


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True, default=None)
    is_active = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tokens = relationship("Token", back_populates="user")
    roles = relationship("Role", secondary=user_roles,
                         back_populates="users", uselist=False, lazy="joined")
