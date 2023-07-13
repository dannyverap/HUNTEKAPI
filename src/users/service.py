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
from src.roles.constants import Role
from src.roles.service import role as role_service
from src.database.base import CRUDBase
from .models import User
from .schemas import UserCreate, UserUpdate
from src.roles.models import user_roles
from src.config import settings


# Pydantic
from pydantic import UUID4, EmailStr


# class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
#     def get_by_id(self, db: Session, *, id: UUID4) -> Optional[User]:
#         return db.query(User).filter(User.id == id).first()

#     def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
#         return db.query(User).filter(User.email == email).first()

#     def create(self, db: Session, *, obj_in: UserCreate) -> User:
#         new_user = {
#             "email": obj_in.email,
#             "password": None,
#             "full_name": obj_in.full_name,
#         }

#         if obj_in.password is not None:
#             new_user["password"] = get_password_hash(obj_in.password)

#         db_obj = User(**new_user)
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         # Assign default role to new user
#         role = role_service.get_by_name(db, name=Role.APPLICANT["name"])
#         role.users.append(db_obj)
#         db.commit()
#         return db_obj

#     def update(
#         self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
#     ) -> User:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True)
#         if update_data["password"]:
#             password = get_password_hash(update_data["password"])
#             del update_data["password"]
#             update_data["password"] = password
#         return super().update(db, db_obj=db_obj, obj_in=update_data)

#     def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
#         user = self.get_by_email(db, email=email)
#         if not user:
#             return None
#         if not verify_password(password, user.password):
#             return None
#         return user

#     def is_active(self, user: User) -> bool:
#         if user.is_active and not user.is_blocked:
#             return True
#         return False

# user = CRUDUser(User)


# -------------------------------------------------------------


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_id(self, db: Session, *, id: UUID4) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, user: UserCreate) -> User:
        new_user = {
            "email": user.email,
            "password": None,
            "first_name": user.first_name,  # habia Error
            "last_name": user.last_name,
        }

        if user.password is not None:
            new_user["password"] = get_password_hash(user.password)

        db_new_user = User(**new_user)
        db.add(db_new_user)
        db.commit()

        db.refresh(db_new_user)
        # Assign default role to new user
        # role = role_service.get_by_name(db, name=Role.APPLICANT["name"])
        # role.users.append(db_obj)

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

      
user = CRUDUser(User)
