from sqlalchemy.orm import Session
from src.files.models import UserFiles
from src.files.schemas import UserFilesCreate, UserFilesUpdate
from src.database.base import CRUDBase
from typing import Optional

class CRUDUserFilesService(CRUDBase[UserFiles, UserFilesCreate, UserFilesUpdate]):
    def create_user_file(self, db: Session, *, user_file_data: UserFilesCreate) -> UserFiles:
        new_user_file = {
            "user_id": user_file_data.user_id,
            "profile_cv": user_file_data.profile_cv,
            "profile_picture": user_file_data.profile_picture,
            "created_at": user_file_data.created_at,
        }
        
        db_obj = UserFiles(**new_user_file)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
        
    def get_user_file_by_user_id(self, db: Session, user_id: str) -> Optional[UserFiles]:
        return db.query(UserFiles).filter(UserFiles.user_id == user_id).first()
    
    def update_user_file(
        self,
        db: Session,
        user_id: str,
        user_file_data: UserFilesUpdate
    ) -> Optional[UserFiles]:
        db_obj = self.get_user_file_by_user_id(db, user_id)
        if db_obj:
            updated_data = user_file_data.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None

    def delete_user_file(self, db: Session, user_id: str) -> Optional[UserFiles]:
        db_obj = self.get_user_file_by_user_id(db, user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None

user_files_service = CRUDUserFilesService(UserFiles)
