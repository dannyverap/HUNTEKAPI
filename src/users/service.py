# Python
from pprint import pprint
from typing import Any, Dict, Optional, Union, List
import random
from datetime import timedelta, datetime
from fastapi_jwt_auth import AuthJWT

# SqlAlchemy
from sqlalchemy.orm import Session

# src utilities
from src.auth.utils import get_password_hash, verify_password
from src.roles.constants import Role as RoleConstants
from src.roles.service import role as role_service
from src.database.base import CRUDBase
from .models import User
from .schemas import UserCreate, UserUpdate
from src.roles.schemas import RoleCreate, Role
from src.config import settings
from src.roles.models import Role, user_roles


# Pydantic
from pydantic import UUID4, EmailStr


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_id(self, db: Session, *, id: UUID4) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, user: UserCreate) -> User:
        new_user = {
            "email": user.email,
            "password": None,
            "first_name": user.first_name, 
            "last_name": user.last_name,
        }

        if user.password is not None:
            new_user["password"] = get_password_hash(user.password)

        db_new_user = User(**new_user)
        db.add(db_new_user)
        # db.commit()

        # db.refresh(db_new_user)
        # # Assign default role to new user
        # # role = role_service.get_by_name(db, name=Role.APPLICANT["name"])
        # # role.users.append(db_obj)
        # new_role = RoleCreate(name=role_name) 
        # db_new_role = Role(**new_role.dict())
        # db.add(db_new_user)
        # db.commit()
        
        # user.roles.append(db_new_role)

        db.commit()
        return db_new_user

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        if user.is_active:
            return True
        return False
    
    def add_role_to_user(self, db: Session, *, role_name: str, user_id: UUID4) -> None:
        user = self.get_by_id(db, id=user_id)
        role = role_service.get_by_name(db, name=role_name)
        
        if not role:
            new_role = RoleCreate(name=role_name)
            role = role_service.create_role(db, role_in=new_role)

        if role not in user.roles:
            user.roles.append(role)
            db.commit()

        

      
user = CRUDUser(User)
