from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.dependencies import get_db
from src.job_applications.schemas import JobApplicationCreate, JobApplicationUpdate, JobApplicationResponse
from src.job_applications.service import JobApplicationService

job_applications_router = APIRouter()

@job_applications_router.post("/job_applications", status_code=status.HTTP_201_CREATED)
def create_job_application(
    job_application: JobApplicationCreate, db: Session = Depends(get_db)
):
    try:
        job_application_service_instance = JobApplicationService(db)
        new_job_application = job_application_service_instance.create_job_application(job_application)
        return new_job_application
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating job application",
        )
    finally:
        db.close()

@job_applications_router.get("/job_applications")
def get_all_job_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_application_service_instance = JobApplicationService(db)
    job_applications = job_application_service_instance.get_all_job_applications(skip, limit)
    return job_applications

@job_applications_router.get("/job_applications/{job_application_id}")
def get_job_application(job_application_id: str, db: Session = Depends(get_db)):
    job_application_service_instance = JobApplicationService(db)
    job_application = job_application_service_instance.get_job_application_by_id(job_application_id)
    if not job_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found")
    return job_application

@job_applications_router.put("/job_applications/{job_application_id}")
def update_job_application(
    job_application_id: str, job_application: JobApplicationUpdate, db: Session = Depends(get_db)
):
    try:
        job_application_service_instance = JobApplicationService(db)
        existing_job_application = job_application_service_instance.update_job_application(job_application_id, job_application)
        return existing_job_application
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while updating job application",
        )
    finally:
        db.close()

@job_applications_router.delete("/job_applications/{job_application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_application(job_application_id: str, db: Session = Depends(get_db)):
    job_application_service_instance = JobApplicationService(db)
    job_application_service_instance.delete_job_application(job_application_id)
    return {"message": "Job application deleted"}
