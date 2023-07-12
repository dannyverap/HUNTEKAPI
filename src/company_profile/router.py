from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.company_profile.models import CompanyProfile
from src.company_profile.schemas import CompanyProfileCreate, CompanyProfileUpdate 
from .service import company_profile_service 
from src.database.base import CRUDBase
from src.dependencies import get_db, get_current_user
from fastapi_jwt_auth import AuthJWT

company_profile_router = APIRouter()

# Función para verificar si el usuario está autenticado
def authenticate_user(current_user: CompanyProfile = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="No está autenticado")
    return current_user

# Función para verificar si el user_id corresponde al usuario autenticado
def validate_user_id(user_id: str, current_user: CompanyProfile = Depends(get_current_user)):
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="No corresponde al usuario")

# Función para verificar si el perfil de usuario no existe
def no_company_profile_exists(db: Session, user_id: str):
    company_profile = company_profile_service.get_company_profile_by_user_id(db, user_id=user_id)
    if company_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return company_profile


# Funcion que verifica si el usuario ya tiene un perfil asignado
def existing_profile(db: Session, user_id: str):
    existing = company_profile_service.get_company_profile_by_user_id(db, user_id=user_id)
    if existing:
        raise HTTPException(status_code=400, detail="El perfil de usuario ya existe")
    return existing

#////////////////////////////////////////////////////////////////////////////

@company_profile_router.post("/company-profiles/{user_id}")
def create_company_profile(
    profile_data: CompanyProfileCreate,
    user_id: str,
    current_user: CompanyProfile = Depends(get_current_user),
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
    created_profile = company_profile_service.create_company_profile(
        db, profile_data=profile_data
    )
    return created_profile

#////////////////////////////////////////////////////////////////////////////

@company_profile_router.get("/company-profiles/{user_id}")
def get_company_profile(
    user_id: str,
    current_user: CompanyProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    return company_profile_service.get_company_profile_by_user_id(db, user_id)

#////////////////////////////////////////////////////////////////////////////

@company_profile_router.put("/user-profiles/{user_id}")
def update_company_profile(
    user_id: str,
    profile_data: CompanyProfileUpdate,
    current_user: CompanyProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    updated_profile = company_profile_service.update_company_profile(db, user_id=user_id, profile_data=profile_data)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return updated_profile

#////////////////////////////////////////////////////////////////////////////

@company_profile_router.delete("/user-profiles/{user_id}")
def delete_company_profile(
    user_id: str,
    current_user: CompanyProfile = Depends(authenticate_user),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    validate_user_id(user_id, current_user)
    deleted_profile = company_profile_service.delete_company_profile(db, user_id=user_id)
    if deleted_profile is None:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")
    return {"message": "Perfil de usuario eliminado exitosamente"}

