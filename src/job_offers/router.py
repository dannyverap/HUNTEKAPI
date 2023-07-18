from fastapi import status, HTTPException, APIRouter, Depends, Request, Body
from typing import Any, Generic, List, Optional
from sqlalchemy.orm import Session
from src.job_offers.schemas import JobOffersBase, JobOffersCreate, JobOffersUpdate
from fastapi.responses import JSONResponse
from src.dependencies import get_db, get_current_user
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import SQLAlchemyError
from src.users.models import User
from src.job_offers.service import job_offer_service

job_offers_router = APIRouter()

@job_offers_router.post("/job_offers/", status_code=status.HTTP_201_CREATED)
def create_job_offer(
    job_offer: JobOffersCreate, user_id: str, db: Session = Depends(get_db)
):
    try:
        job_offer_service_instance = job_offer_service(db)
        new_job_offer = job_offer_service_instance.create_job_offer(job_offer, user_id)
        return new_job_offer
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating job offer",
        )
    finally:
        db.close()


@job_offers_router.get("/job_offers", response_model=List[JobOffersBase])
def get_all_job_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_offer_service_instance = job_offer_service(db)
    job_offers = job_offer_service_instance.get_all_job_offers(skip, limit)
    return job_offers



@job_offers_router.get("/job_offers/user/{user_id}", response_model=List[JobOffersBase])
def get_job_offers_by_user_id(user_id: str, db: Session = Depends(get_db)):
    job_offer_service_instance = job_offer_service(db)
    job_offers = job_offer_service_instance.get_job_offers_by_user_id(user_id)
    return job_offers


@job_offers_router.get("/job_offers/company/{company_id}", response_model=List[JobOffersBase])
def get_job_offers_by_company_id(company_id: str, db: Session = Depends(get_db)):
    job_offer_service_instance = job_offer_service(db)
    job_offers = job_offer_service_instance.get_job_offers_by_company_id(company_id)
    return job_offers


@job_offers_router.get("/job_offers/{offer_id}", response_model=JobOffersBase)
def get_job_offer_by_offer_id(offer_id: str, db: Session = Depends(get_db)):
    job_offer_service_instance = job_offer_service(db)
    job_offer = job_offer_service_instance.get_job_offer_by_offer_id(offer_id)
    if not job_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job offer not found",
        )
    return job_offer


@job_offers_router.put("/job_offers/{offer_id}", status_code=status.HTTP_200_OK)
def update_job_offer(
    offer_id: str, job_offer: JobOffersUpdate, db: Session = Depends(get_db)
):
    job_offer_service_instance = job_offer_service(db)
    existing_job_offer = job_offer_service_instance.update_job_offer(offer_id, job_offer)
    return existing_job_offer


@job_offers_router.delete("/job_offers/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_offer(offer_id: str, db: Session = Depends(get_db)):
    job_offer_service_instance = job_offer_service(db)
    job_offer_service_instance.delete_job_offer(offer_id)
    return None


@job_offers_router.get("/hola")
def ping():
    return JSONResponse(content={"success": True, "msg": "Base module installed!"})
