from uuid import uuid4

from src.database.base import Base
from sqlalchemy import Table,Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
)


class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(100), index=True)
    description = Column(Text)
    users = relationship("User", secondary=user_roles, back_populates="roles")