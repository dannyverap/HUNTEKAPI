from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate
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
        raise HTTPException(status_code=401, detail="No está autenticado")

    # Verificar que el user_id corresponde al usuario autenticado
    if profile_data.user_id != user_id:
        raise HTTPException(status_code=403, detail="No corresponde al usuario")
    
    # Crear el perfil de usuario utilizando el servicio
    created_profile = user_profile_service.create_user_profile(db, profile_data=profile_data)
    
    return created_profile

@user_profile_router.get("/user-profiles/{user_id}")
def get_user_profile (
    user_id: str,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    # Aquí puedes verificar si el usuario está autenticado
    if current_user is None:
        raise HTTPException(status_code=401, detail="No está autenticado")

    # Verificar que el user_id corresponde al usuario autenticado
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="No corresponde al usuario")
    
    # Obtiene el perfil de usuario utilizando el servicio
    user_profile = user_profile_service.get_user_profile_by_user_id(db, user_id=user_id)
    
    if user_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    
    return user_profile

@user_profile_router.put("/user-profiles/{user_id}")
def update_user_profile (
    user_id: str,
    profile_data: UserProfileUpdate,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    # Aquí puedes verificar si el usuario está autenticado
    if current_user is None:
        raise HTTPException(status_code=401, detail="No está autenticado")

    # Verificar que el user_id corresponde al usuario autenticado
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="No corresponde al usuario")
    
    # Actualizar el perfil de usuario utilizando el servicio
    updated_profile = user_profile_service.update_user_profile(db, user_id=user_id, profile_data=profile_data)
    
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    
    return updated_profile

@user_profile_router.delete("/user-profiles/{user_id}")
def delete_user_profile(
    user_id: str,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    # Aquí puedes verificar si el usuario está autenticado
    if current_user is None:
        raise HTTPException(status_code=401, detail="No está autenticado")

    # Verificar que el user_id corresponde al usuario autenticado
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="No corresponde al usuario")
    
    # Eliminar el perfil de usuario utilizando el servicio
    deleted_profile = user_profile_service.delete_user_profile(db, user_id=user_id)
    
    if deleted_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    
    return {"message": "Perfil de usuario eliminado exitosamente"}


