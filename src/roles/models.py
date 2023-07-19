# Python
from uuid import uuid4

# SqlAlchemy
from sqlalchemy import Table,Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Choice, ChoiceType

# SrcUtilities
from src.database.base import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
)


class Role(Base):
    ROLE_NAME=(
        ("admin", "admin"),
        ("applicant", "applicant"),
        ("company", "company"),
        ("company_recruiter", "company_recruiter"),
    )
    
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(ChoiceType(ROLE_NAME), default="APPLICANT")
    description = Column(Text)
    users = relationship("User", secondary=user_roles, back_populates="roles", uselist= True, lazy="joined")
    