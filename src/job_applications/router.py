from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.dependencies import get_db
from src.job_applications.models import JobApplication
from src.job_applications.schemas import JobApplicationCreate, JobApplicationUpdate, JobApplicationResponse

job_applications_router = APIRouter()

@job_applications_router.post("/job_applications", response_model=JobApplicationResponse)
def create_job_application(job_application: JobApplicationCreate, db: Session = Depends(get_db)):
    new_job_application = JobApplication(**job_application.dict())
    db.add(new_job_application)
    db.commit()
    db.refresh(new_job_application)
    return new_job_application

@job_applications_router.get("/job_applications", response_model=List[JobApplicationResponse])
def get_all_job_applications(db: Session = Depends(get_db)):
    job_applications = db.query(JobApplication).all()
    return job_applications

@job_applications_router.get("/job_applications/{job_application_id}", response_model=JobApplicationResponse)
def get_job_application(job_application_id: str, db: Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    return job_application

@job_applications_router.put("/job_applications/{job_application_id}", response_model=JobApplicationResponse)
def update_job_application(job_application_id: str, job_application: JobApplicationUpdate, db: Session = Depends(get_db)):
    existing_job_application = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
    if not existing_job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    for field, value in job_application.dict(exclude_unset=True).items():
        setattr(existing_job_application, field, value)
    db.commit()
    db.refresh(existing_job_application)
    return existing_job_application

@job_applications_router.delete("/job_applications/{job_application_id}")
def delete_job_application(job_application_id: str, db: Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    db.delete(job_application)
    db.commit()
    return {"message": "Job application deleted"}
