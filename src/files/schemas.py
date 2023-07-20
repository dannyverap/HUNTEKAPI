from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


# Definimos el esquema Pydantic para UserFiles
class UserFilesBase(BaseModel):
    id: Optional[UUID4]
    user_id: Optional[UUID4]
    profile_cv: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        
class UserFilesCreate(UserFilesBase):
    pass

class UserFilesUpdate(UserFilesBase):
    pass

