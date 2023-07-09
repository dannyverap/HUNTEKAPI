# FastAPI
# from fastapi import Body, Depends, BackgroundTasks, Query, Request
# from fastapi import status, HTTPException, APIRouter, Security
# from fastapi.responses import JSONResponse


# user_profile_router = APIRouter()

# @user_profile_router.get("/user_profile")
# async def get_user_profile(
#     db: Session = Depends(get_db),
#     skip: int = 0,
#     limit: int = 100,
#     ##! current user?
# )
#     :
#     return JSONResponse(content={"success":True,"msg":"Base module installed!"})

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from src.dependencies import get_db
from src.user_profile.service import UserProfileService
from src.user_profile.schemas import UserProfile, UserProfileCreate, UserProfileUpdate

router = APIRouter()


@router.post("/user-profiles/", response_model=UserProfile)
def create_user_profile(
    user_id: UUID,
    profile: UserProfileCreate,
    db: Session = Depends(get_db),
    profile_service: UserProfileService = Depends()
) -> UserProfile:
    return profile_service.create_user_profile(user_id, profile)


@router.get("/user-profiles/{user_id}", response_model=UserProfile)
def get_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    profile_service: UserProfileService = Depends()
) -> UserProfile:
    return profile_service.get_user_profile(user_id)


@router.put("/user-profiles/{user_id}", response_model=UserProfile)
def update_user_profile(
    user_id: UUID,
    profile: UserProfileUpdate,
    db: Session = Depends(get_db),
    profile_service: UserProfileService = Depends()
) -> UserProfile:
    return profile_service.update_user_profile(user_id, profile)


@router.delete("/user-profiles/{user_id}")
def delete_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    profile_service: UserProfileService = Depends()
) -> None:
    profile_service.delete_user_profile(user_id)
