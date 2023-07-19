from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.interviews.schemas import InterviewsCreate, InterviewsUpdate, Interviews
from .service import interviews_service

interviews_router = APIRouter()

@interviews_router.post("/interviews/{profile_id}")
def create_interview(
    interview_data: InterviewsCreate,
    profile_id: str,
    db: Session = Depends(get_db),
    
):
    interview_data.profile_id = profile_id
    interview = interviews_service.create_interviews(db, profile_data=interview_data)
    return interview

@interviews_router.get("/interviews/{profile_id}")
def get_interviews_by_profile_id(
    profile_id: str,
    db: Session = Depends(get_db)
):
    interviews = interviews_service.get_interviews_by_profile_id(db, profile_id=profile_id)
    if not interviews:
        raise HTTPException(status_code=404, detail="No se encontraron entrevistas para el usuario")
    return interviews

@interviews_router.put("/interviews/{interview_id}")
def update_interview(
    interview_id: str,
    interview_data: InterviewsUpdate,
    db: Session = Depends(get_db)
):
    interview = interviews_service.update_interview(db, interview_id, interview_data)
    if not interview:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    return interview

@interviews_router.delete("/interviews/{interview_id}")
def delete_interview(
    interview_id: str,
    db: Session = Depends(get_db)
):
    interview = interviews_service.delete_interview(db, interview_id=interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    return {"message": "Entrevista eliminada exitosamente"}

 


