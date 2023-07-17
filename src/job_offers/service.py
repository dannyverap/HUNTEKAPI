from typing import List, Optional
from sqlalchemy.orm import Session
from src.job_offers.models import JobOffer
from src.job_offers.schemas import JobOffersCreate, JobOffersUpdate
from src.users.models import User
from src.database.base import CRUDBase
from fastapi import HTTPException, status, Depends

class job_offer_service:
    def __init__(self, db: Session):
        self.db = db
        self.job_offer_crud = CRUDBase(JobOffer)

    def create_job_offer(self, job_offer: JobOffersCreate, user_id: str) -> JobOffer:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        
        company_profile = user.company_profile
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company profile not found for the user",
            )

        new_job_offer = JobOffer(
            job_title=job_offer.job_title,
            description=job_offer.description,
            modality=job_offer.modality,
            work_schedule=job_offer.work_schedule,
            requirements=job_offer.requirements,
            postulants=job_offer.postulants,
            user=user,
            company_profile=company_profile,
        )
        
        self.db.add(new_job_offer)
        self.db.commit()
        self.db.refresh(new_job_offer)
        
        return new_job_offer

    def get_all_job_offers(self) -> List[JobOffer]:
        job_offers = self.db.query(JobOffer).all()
        return job_offers

    def get_job_offers_by_user_id(self, user_id: str) -> List[JobOffer]:
        job_offers = self.db.query(JobOffer).filter(JobOffer.user_id == user_id).all()
        return job_offers

    def get_job_offers_by_company_id(self, company_id: str) -> List[JobOffer]:
        job_offers = self.db.query(JobOffer).filter(JobOffer.company_profile_id == company_id).all()
        return job_offers

    def get_job_offer_by_offer_id(self, offer_id: str) -> Optional[JobOffer]:
        job_offer = self.db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        return job_offer

    def update_job_offer(self, offer_id: str, job_offer: JobOffersUpdate) -> JobOffer:
        existing_job_offer = self.db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not existing_job_offer:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job offer not found",
        )

        updated_data = job_offer.dict(exclude_unset=True)  # Obtener solo los campos actualizados
        for key, value in updated_data.items():
            setattr(existing_job_offer, key, value)

        self.db.commit()
        self.db.refresh(existing_job_offer)

        return existing_job_offer

    def delete_job_offer(self, offer_id: str) -> None:
        existing_job_offer = self.db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not existing_job_offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job offer not found",
            )

        self.db.delete(existing_job_offer)
