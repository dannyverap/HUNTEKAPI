from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from src.files.schemas import UserFilesCreate
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.files.service import user_files_service
import boto3
import os

files_router = APIRouter()


AWS_BUCKET_NAME = "your-aws-bucket-name"
AWS_REGION_NAME = "your-aws-region-name"
AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"

# Función para subir el archivo al bucket de S3 y obtener la URL
def upload_file_to_s3(file: UploadFile, folder_name: str):
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    file_name = f"{folder_name}/{file.filename}"
    s3.upload_fileobj(file.file, AWS_BUCKET_NAME, file_name)

    url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{file_name}"
    return url

@files_router.post("/upload/")
async def upload_files(user_id: str, cv: UploadFile = File(None), profile_picture: UploadFile = File(None)):
    db = get_db()

    user_files_data = UserFilesCreate(user_id=user_id)

    if cv:
        cv_url = upload_file_to_s3(cv, folder_name="cv")
        user_files_data.profile_cv = cv_url

    if profile_picture:
        profile_picture_url = upload_file_to_s3(profile_picture, folder_name="profile_picture")
        user_files_data.profile_picture = profile_picture_url

    # Guardar la información en la base de datos utilizando el servicio CRUDUserFilesService
    user_files_service.create_user_file(db=db, user_file_data=user_files_data)

    return {"message": "Files uploaded successfully."}

