
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.files.service import user_files_service
from src.files.schemas import UserFilesBase, UserFilesCreate, UserFilesUpdate

files_router = APIRouter()

@files_router.post("/archivos_usuario/", response_model=UserFilesBase)
def crear_archivo_usuario(
    user_file_data: UserFilesCreate, db: Session = Depends(get_db)
):
    return user_files_service.create_user_file(db, user_file_data=user_file_data)

@files_router.get("/archivos_usuario/{user_id}", response_model=UserFilesBase)
def leer_archivo_usuario(user_id: str, db: Session = Depends(get_db)):
    user_file = user_files_service.get_user_file_by_user_id(db, user_id)
    if user_file is None:
        raise HTTPException(status_code=404, detail="Archivo de usuario no encontrado")
    return user_file

@files_router.put("/archivos_usuario/{user_id}", response_model=UserFilesBase)
def actualizar_archivo_usuario(
    user_id: str, user_file_data: UserFilesUpdate, db: Session = Depends(get_db)
):
    updated_user_file = user_files_service.update_user_file(db, user_id, user_file_data)
    if updated_user_file is None:
        raise HTTPException(status_code=404, detail="Archivo de usuario no encontrado")
    return updated_user_file

@files_router.delete("/archivos_usuario/{user_id}", response_model=UserFilesBase)
def eliminar_archivo_usuario(user_id: str, db: Session = Depends(get_db)):
    deleted_user_file = user_files_service.delete_user_file(db, user_id)
    if deleted_user_file is None:
        raise HTTPException(status_code=404, detail="Archivo de usuario no encontrado")
    return deleted_user_file
