from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
import datetime
from src.database.base import Base

class UserFiles(Base):
    __tablename__ = "user_files"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    profile_cv = Column(String)
    profile_picture = Column(String)  # Columna para almacenar la clave del objeto en S3
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="user_files", uselist=False)
    
    