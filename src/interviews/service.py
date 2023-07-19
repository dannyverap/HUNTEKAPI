from sqlalchemy.orm import Session
from src.interviews.models import Interviews
from src.interviews.schemas import InterviewsCreate, InterviewsUpdate
from src.database.base import CRUDBase
from typing import Optional, List

class CRUDInterviewsService(CRUDBase[Interviews, InterviewsCreate, InterviewsUpdate]):
    def create_interviews(
        self, db: Session,*, interview_data: InterviewsCreate) -> Interviews:
        new_interview = {
            "user_id" : interview_data.user_id,
            "job_position": interview_data.job_position,
            "interviewr_name": interview_data.interviewr_name,
            "online_link": interview_data.online_link,
            "date": interview_data.date,
            "company_profile_id": interview_data.company_profile_id,
        }
        db_obj = Interviews(**new_interview)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_all_interviews(self, db: Session) -> List[Interviews]:
        return db.query(Interviews).all()
    
    def get_interview_by_id(self, db: Session, interview_id: str) -> Optional[Interviews]:
        return db.query(Interviews).filter(Interviews.id == interview_id).first()
    
    
    def get_interviews_by_user_id(self, db: Session, user_id: str) -> List[Interviews]:
        return db.query(Interviews).filter(Interviews.user_id== user_id).all()
    
    
    def get_interviews_by_company_profile_id(self, db: Session, company_profile_id: str) -> List[Interviews]:
        return db.query(Interviews).filter(Interviews.company_profile_id == company_profile_id).all()
    
    
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