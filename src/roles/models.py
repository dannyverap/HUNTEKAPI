from uuid import uuid4

from src.database.base import Base
from sqlalchemy import Table,Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Choice, ChoiceType


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
)

# admin_roles = Table(
#     "admin_roles",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
#     Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
# )

# applicant_roles = Table(
#     "applicant_roles",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
#     Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
# )

# company_roles = Table(
#     "company_roles",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
#     Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
# )

# company_recruiter_roles = Table(
#     "company_recruiter_roles",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
#     Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
# )


class Role(Base):
    ROLE_NAME=(
        ("ADMIN", "admin"),
        ("APPLICANT", "applicant"),
        ("COMPANY", "company"),
        ("COMPANY_RECRUITER", "company_recruiter"),
    )
    
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(ChoiceType(ROLE_NAME), default="APPLICANT")
    description = Column(Text)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
# class Role(Base):
#     __tablename__ = "roles"
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
#     users = relationship("User", secondary=[admin_roles, applicant_roles, company_roles, company_recruiter_roles], back_populates="roles")
        