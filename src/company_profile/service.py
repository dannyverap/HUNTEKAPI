from sqlalchemy.orm import Session
from src.company_profile.models import CompanyProfile
from src.company_profile.schemas import CompanyProfileCreate, CompanyProfileUpdate
from src.database.base import CRUDBase
from typing import Any, Generic, List, Optional

class CRUDCompanyProfileService(CRUDBase[CompanyProfile, CompanyProfileCreate, CompanyProfileUpdate]):
    def create_company_profile(self, db: Session,*, profile_data: CompanyProfileCreate)-> CompanyProfile:
        new_profile = {
            "user_id": profile_data.user_id,
            "company_logo": profile_data.company_logo,
            "company_description": profile_data.company_description,
            "company_why_us": profile_data.company_why_us,
            "company_know_us_better_video": profile_data.company_know_us_better_video,
            "job_offers": profile_data.job_offers,
            "interviews": profile_data.interviews,
        }
        
        db_obj = CompanyProfile(**new_profile)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
        
    def get_company_profile_by_user_id(self, db: Session, user_id: str) -> Optional[CompanyProfile]:
        return db.query(CompanyProfile).filter(CompanyProfile.user_id == user_id).first()
    
    def update_company_profile(
        self,
        db: Session,
        user_id: str,
        profile_data: CompanyProfileUpdate
    ) -> Optional[CompanyProfile]:
        db_obj = self.get_company_profile_by_user_id(db, user_id)
        if db_obj:
            updated_data = profile_data.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None

    def delete_company_profile(self, db: Session, user_id: str) -> Optional[CompanyProfile]:
        db_obj = self.get_company_profile_by_user_id(db, user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None
    
company_profile_service = CRUDCompanyProfileService(CompanyProfile)


