from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from src.database.base import CRUDBase
from typing import Any, Generic, List, Optional

class CRUDUserProfileService(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    def create_user_profile(self, db: Session,*, profile_data: UserProfileCreate)-> UserProfile:
        new_profile = {
            "user_id": profile_data.user_id,
            "profile_picture": profile_data.profile_picture,
            "applications": profile_data.applications,
            # "interviews": profile_data.interviews,
            "responses": profile_data.responses,
            "phone_number": profile_data.phone_number,
            "resume": profile_data.resume,
        }
        
        db_obj = UserProfile(**new_profile)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
        
    def get_user_profile_by_user_id(self, db: Session, user_id: str) -> Optional[UserProfile]:
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    def update_user_profile(
        self,
        db: Session,
        user_id: str,
        profile_data: UserProfileUpdate
    ) -> Optional[UserProfile]:
        db_obj = self.get_user_profile_by_user_id(db, user_id)
        if db_obj:
            updated_data = profile_data.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None

    def delete_user_profile(self, db: Session, user_id: str) -> Optional[UserProfile]:
        db_obj = self.get_user_profile_by_user_id(db, user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None
    
user_profile_service = CRUDUserProfileService(UserProfile)


