
from sqlalchemy.orm import Session
from src.user_profile.models import UserProfile
from src.user_profile.schemas import UserProfileCreate, UserProfileUpdate
from src.database.base import CRUDBase

class CRUDUserProfileService(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    def create_user_profile(self, db: Session,*, profile_data: UserProfileCreate)-> UserProfile:
        new_profile = {
            "user_id": profile_data.user_id,
            "profile_picture": profile_data.profile_picture,
            "applications": profile_data.applications,
            "interviews": profile_data.interviews,
            "responses": profile_data.responses,
            "phone_number": profile_data.phone_number,
            "resume": profile_data.resume,
        }
        
        db_obj = UserProfile(**new_profile)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
user_profile_service = CRUDUserProfileService(UserProfile)

