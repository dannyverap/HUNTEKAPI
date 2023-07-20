from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.interviews.schemas import InterviewsCreate, InterviewsUpdate, InterviewsBase
from .service import interviews_service
from src.users.models import User
from src.dependencies import get_db, get_current_user
from src.users.service import user
from typing import List

interviews_router = APIRouter()

@interviews_router.get("/interview/{interview_id}", response_model=InterviewsBase)
def get_interview_by_id(
    interview_id: str,
    db: Session = Depends(get_db)
):
    interview = interviews_service.get_interview_by_id(db,interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found") 
    return interview

# Función para verificar si el usuario está autenticado
def authenticate_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

# Función para verificar si el user_id corresponde al usuario autenticado
def validate_user_id(user_id: str, current_user: User = Depends(get_current_user)):
    if user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not applicable to the user")

# Función para verificar si el usuario no existe
def no_user_exists(db: Session, user_id: str):
    user_exist = user.get_by_id(db, user_id=user_id)
    if user_exist is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user


@interviews_router.post("/new_interview/{user_id}")
def create_interview(
    interview_data: InterviewsCreate,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    
):

    authenticate_user(current_user)
  
    validate_user_id(user_id, current_user)
    
    interview_data.user_id = user_id
    interview = interviews_service.create_interviews(db, interview_data=interview_data)
    return interview

@interviews_router.get("/user_interviews/{user_id}")
def get_interviews_by_user_id(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interviews = interviews_service.get_interviews_by_user_id(db, user_id=user_id)
    validate_user_id(user_id, current_user)
    return interviews

@interviews_router.put("/update/{interview_id}")
def update_interview(
    
    interview_id: str,
    interview_data: InterviewsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    authenticate_user(current_user)
    interview = interviews_service.update_interview(db, interview_id, interview_data)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@interviews_router.delete("/delete/{interview_id}")
def delete_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    authenticate_user(current_user)
    interview = interviews_service.delete_interview(db, interview_id=interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return {"message": "Interview successfully deleted"}




@interviews_router.get("/company_interviews/{company_profile_id}")
def get_interviews_by_company_profile_id(
    company_profile_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interviews = interviews_service.get_interviews_by_company_profile_id(db, company_profile_id=company_profile_id)
    return interviews

@interviews_router.get("/all/", response_model=List[InterviewsBase])
def get_all_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    interviews = interviews_service.get_all_interviews(db)
    return interviews

