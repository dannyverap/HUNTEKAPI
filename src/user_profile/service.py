from sqlalchemy.orm import Session
from src.user_profile.models import user_profile as UserProfileModel
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from pydantic import UUID4

class UserProfileService:
    def __init__(self, db: Session):
        self.db = db

    def create_user_profile(self, user_id: UUID4, profile: UserProfileCreate) -> UserProfileModel:
        profile_data = UserProfileModel(user_id=user_id, **profile.dict())
        self.db.add(profile_data)
        self.db.commit()
        self.db.refresh(profile_data)
        return profile_data

    def get_user_profile(self, user_id: UUID4) -> UserProfileModel:
        return self.db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()

    def update_user_profile(self, user_id: UUID4, profile: UserProfileUpdate) -> UserProfileModel:
        profile_data = self.get_user_profile(user_id)
        for field, value in profile.dict().items():
            setattr(profile_data, field, value)
        self.db.commit()
        self.db.refresh(profile_data)
        return profile_data

    def delete_user_profile(self, user_id: UUID4) -> None:
        profile_data = self.get_user_profile(user_id)
        self.db.delete(profile_data)
        self.db.commit()
