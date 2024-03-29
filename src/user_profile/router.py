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


#////////////////////////////////////////////////////////////////////////////

from fastapi import UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
UPLOAD_FOLDER = "profile pictures"

@user_profile_router.post("/user-profiles/{user_id}/subir-foto-perfil")
async def subir_foto_perfil(
    user_id: str,
    foto_perfil: UploadFile = File(...),
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
    # Verifica que el user_id corresponde al usuario autenticado
    validate_user_id(user_id, current_user)

    # Crea la ruta completa para guardar la foto de perfil
    ruta_guardado = os.path.join(UPLOAD_FOLDER, foto_perfil.filename)

    # Guarda la foto de perfil en la carpeta de destino
    with open(ruta_guardado, "wb") as archivo_destino:
        shutil.copyfileobj(foto_perfil.file, archivo_destino)

    # Actualiza el campo de la foto de perfil en la base de datos
    perfil_usuario = user_profile_service.get_user_profile_by_user_id(db, user_id)
    perfil_usuario.profile_picture = ruta_guardado
    db.commit()

    return {"mensaje": "Foto de perfil subida exitosamente"}

#////////////////////////////////////////////////////////////////////////////

@user_profile_router.get("/user-profiles/{user_id}/profile-picture")
async def get_profile_picture(
    user_id: str,
    current_user: UserProfile = Depends(authenticate_user),
    db: Session = Depends(get_db)
    ):
    # Verifica si el usuario tiene un perfil de usuario
    validate_user_id(user_id,current_user)
    user_profile = user_profile_service.get_user_profile_by_user_id(db, user_id)
    

    # Obtiene la ruta de la imagen de perfil almacenada
    profile_picture_path = user_profile.profile_picture
    if not profile_picture_path:
        raise HTTPException(status_code=404, detail="Imagen de perfil no encontrada")

    # Verifica si la ruta de la imagen existe en el sistema de archivos
    if not os.path.exists(profile_picture_path):
        raise HTTPException(status_code=404, detail="Imagen de perfil no encontrada")

    # Devuelve la imagen de perfil como una respuesta de archivo
    return FileResponse(profile_picture_path, media_type="image/jpeg")




