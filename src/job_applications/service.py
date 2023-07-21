from typing import List, Optional
from sqlalchemy.orm import Session, selectinload, joinedload
from src.job_applications.models import JobApplication
from src.job_applications.schemas import JobApplicationCreate, JobApplicationUpdate
from src.database.base import CRUDBase
from fastapi import HTTPException, status, Depends
from src.job_offers.models import JobOffer
from src.user_profile.models import UserProfile

class JobApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.job_application_crud = CRUDBase(JobApplication)

    def create_job_application(self, job_application: JobApplicationCreate) -> JobApplication:
        new_job_application = JobApplication(**job_application.dict())
        self.db.add(new_job_application)
        self.db.commit()
        self.db.refresh(new_job_application)
        return new_job_application

    def get_all_job_applications(self, skip: int = 0, limit: int = 100) -> List[JobApplication]:
        job_applications = (
            self.db.query(JobApplication)
            .join(JobOffer)  # Join para traer información de JobOffer
            .join(UserProfile)  # Join para traer información de UserProfile
            .options(
                selectinload(JobApplication.job_offer),
                selectinload(JobApplication.user_profile)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return job_applications

    def get_job_application_by_id(self, job_application_id: str) -> Optional[JobApplication]:
        job_application = (
            self.db.query(JobApplication)
            .filter(JobApplication.id == job_application_id)
            .options(
                joinedload(JobApplication.job_offer),
                joinedload(JobApplication.user_profile)
            )
            .first()
        )
        return job_application

    def update_job_application(self, job_application_id: str, job_application: JobApplicationUpdate) -> JobApplication:
        existing_job_application = self.db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
        if not existing_job_application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job application not found",
            )

        updated_data = job_application.dict(exclude_unset=True)  # Obtener solo los campos actualizados
        for key, value in updated_data.items():
            setattr(existing_job_application, key, value)

        self.db.commit()
        self.db.refresh(existing_job_application)

        return existing_job_application

    def delete_job_application(self, job_application_id: str) -> None:
        existing_job_application = self.db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
        if not existing_job_application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job application not found",
            )

        self.db.delete(existing_job_application)
