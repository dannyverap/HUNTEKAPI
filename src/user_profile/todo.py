from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from src.database.base import Base
from src.users.models import User
import datetime
from sqlalchemy.dialects.postgresql import UUID, BYTEA

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    profile_picture = Column(BYTEA) 
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
    user = relationship("User", back_populates="user_profile", uselist=False)
    
    ESTE ES MI MODELO
    
from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    profile_picture: Optional[str]
    applications: List[str]
    interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserProfileCreate(UserProfileBase):
    profile_picture: Optional[str]
    applications: List[str]
    interviews: List[str]
    responses: str
    phone_number: str
    resume: str
    created_at: datetime
    updated_at: datetime
    
    
class UserProfileUpdate(UserProfileBase):
    pass

ESTE ES MI SCHEMA

from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from src.database.base import CRUDBase
from typing import Any, Generic, List, Optional

class CRUDUserProfileService(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    def create_user_profile(self, db: Session,*, profile_data: UserProfileCreate)-> UserProfile:
        new_profile = {
            "user_id": profile_data.user_id,
            "profile_picture": profile_data.profile_picture,
            "applications": profile_data.applications,
            "interviews": profile_data.interviews,
            "responses": profile_data.responses,
            "phone_number": profile_data.phone_number,
            "resume": profile_data.resume,
        }
        
        db_obj = UserProfile(**new_profile)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
        
    def get_user_profile_by_user_id(self, db: Session, user_id: str) -> Optional[UserProfile]:
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    def update_user_profile(
        self,
        db: Session,
        user_id: str,
        profile_data: UserProfileUpdate
    ) -> Optional[UserProfile]:
        db_obj = self.get_user_profile_by_user_id(db, user_id)
        if db_obj:
            updated_data = profile_data.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None

    def delete_user_profile(self, db: Session, user_id: str) -> Optional[UserProfile]:
        db_obj = self.get_user_profile_by_user_id(db, user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None
    
user_profile_service = CRUDUserProfileService(UserProfile)


ESTE ES MI SERVICE 


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate 
from .service import user_profile_service 
from src.database.base import CRUDBase
from src.dependencies import get_db, get_current_user
from fastapi_jwt_auth import AuthJWT

user_profile_router = APIRouter()

# Función para verificar si el usuario está autenticado
def authenticate_user(current_user: UserProfile = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="No está autenticado")
    return current_user

# Función para verificar si el user_id corresponde al usuario autenticado
def validate_user_id(user_id: str, current_user: UserProfile = Depends(get_current_user)):
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="No corresponde al usuario")

# Función para verificar si el perfil de usuario no existe
def no_user_profile_exists(db: Session, user_id: str):
    user_profile = user_profile_service.get_user_profile_by_user_id(db, user_id=user_id)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return user_profile


# Funcion que verifica si el usuario ya tiene un perfil asignado
def existing_profile(db: Session, user_id: str):
    existing = user_profile_service.get_user_profile_by_user_id(db, user_id=user_id)
    if existing:
        raise HTTPException(status_code=400, detail="El perfil de usuario ya existe")
    return existing

#////////////////////////////////////////////////////////////////////////////

@user_profile_router.post("/user-profiles/{user_id}")
def create_user_profile(
    profile_data: UserProfileCreate,
    user_id: str,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    # Aquí puedes verificar si el usuario está autenticado
    authenticate_user(current_user)
    # Verificar que el user_id corresponde al usuario autenticado
    validate_user_id(user_id, current_user)
    # Verifica si el usuario ya tiene un perfil creaddo
    existing_profile(db, user_id)
    
    profile_data.user_id = user_id
    # Crear el perfil de usuario utilizando el servicio
    created_profile = user_profile_service.create_user_profile(
        db, profile_data=profile_data
    )
    return created_profile

#////////////////////////////////////////////////////////////////////////////

@user_profile_router.get("/user-profiles/{user_id}")
def get_user_profile(
    user_id: str,
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    return user_profile_service.get_user_profile_by_user_id(db, user_id)

#////////////////////////////////////////////////////////////////////////////

@user_profile_router.put("/user-profiles/{user_id}")
def update_user_profile(
    user_id: str,
    profile_data: UserProfileUpdate,
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    updated_profile = user_profile_service.update_user_profile(db, user_id=user_id, profile_data=profile_data)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return updated_profile

#////////////////////////////////////////////////////////////////////////////

@user_profile_router.delete("/user-profiles/{user_id}")
def delete_user_profile(
    user_id: str,
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    deleted_profile = user_profile_service.delete_user_profile(db, user_id=user_id)
    if deleted_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return {"message": "Perfil de usuario eliminado exitosamente"}




ESTAS SON MIS RUTAS