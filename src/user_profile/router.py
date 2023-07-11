
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate
from .service import user_profile_service 
from src.database.base import CRUDBase
from src.dependencies import get_db, get_current_user
from fastapi_jwt_auth import AuthJWT

user_profile_router = APIRouter()

@user_profile_router.get("/saludo")
def saludar():
    return "Hola"


@user_profile_router.post("/user-profiles/{user_id}")
def create_user_profile(
    profile_data: UserProfileCreate,
    user_id: str,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    # Aquí puedes verificar si el usuario está autenticado
    if current_user is None:
        raise HTTPException(status_code=401, detail="No esta autenticado")

    # Verificar que el user_id corresponde al usuario autenticado
    # if profile_data.user_id != user_id:
    #     raise HTTPException(status_code=403, detail="No corresponde al usuario")
    
    profile_data.user_id = user_id
    # Crear el perfil de usuario utilizando el servicio
    created_profile = user_profile_service.create_user_profile(
        db, profile_data=profile_data
    )
    
    return created_profile


