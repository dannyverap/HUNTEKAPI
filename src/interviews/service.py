from sqlalchemy.orm import Session
from src.interviews.models import Interviews
from src.interviews.schemas import InterviewsCreate, InterviewsUpdate
from src.database.base import CRUDBase
from typing import Optional, List

class CRUDInterviewsService(CRUDBase[Interviews, InterviewsCreate, InterviewsUpdate]):
    def create_interviews(
        self, db: Session,*, profile_data: InterviewsCreate) -> Interviews:
        new_interview = {
            "profile_id": profile_data.profile_id,
            "interview_type": profile_data.interview_type,
            "interview_name": profile_data.interview_name,
            "online_link": profile_data.online_link,
            "date": profile_data.date,
            "notes": profile_data.notes,
        }
        db_obj = Interviews(**new_interview)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
    def get_interviews_by_profile_id(self, db: Session, profile_id: str) -> List[Interviews]:
        return db.query(Interviews).filter(Interviews.profile_id == profile_id).all()
    
    
    def update_interview(
        self,
        db: Session,
        interview_id: str,
        interview_data: InterviewsUpdate
    ) -> Optional[Interviews]:
        db_obj = self.get(db, interview_id)
        if db_obj:
            updated_data = interview_data.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None
    
    
    def delete_interview(self, db: Session, interview_id: str) -> Optional[Interviews]:
        db_obj = self.get(db, interview_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None
    
interviews_service = CRUDInterviewsService(Interviews)