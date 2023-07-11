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

# Función para obtener el perfil de usuario
def get_user_profile(db: Session, user_id: str):
    user_profile = user_profile_service.get_user_profile_by_user_id(db, user_id=user_id)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return user_profile


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

@user_profile_router.get("/user-profiles/{user_id}")
def get_user_profile(
    user_id: str,
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    return user_profile_service.get_user_profile_by_user_id(db, user_id)

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

