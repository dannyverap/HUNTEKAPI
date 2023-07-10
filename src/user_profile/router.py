
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate
from .service import user_profile_service 
from src.database.base import CRUDBase
from src.dependencies import get_db


user_profile_router = APIRouter()

@user_profile_router.get("/saludo")
def saludar():
    return "Hola"
#-----------------------------

@user_profile_router.post("/user-profiles")
def create_user_profile(profile_data: UserProfileCreate, db: Session = Depends(get_db)):
    # Crear el perfil de usuario utilizando el servicio
    created_profile = user_profile_service.create_user_profile(db, profile_data=profile_data)
    return created_profile

