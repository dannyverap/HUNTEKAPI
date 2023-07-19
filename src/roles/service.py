# Python
from typing import Optional, List

# Pydantic
from pydantic import UUID4

# SqlAlchemy
from sqlalchemy.orm import Session

# SrcUtilities
from src.database.base import CRUDBase
from src.roles.models import Role, user_roles
from src.roles.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        role = db.query(self.model).filter(Role.name == name).first()
        return role
    
    def get_by_user_id(self, db: Session, *, user_id: UUID4) -> List[Optional[Role]]:
        roles = db.query(user_roles).filter(user_id == user_id).all()
        
        role_names = []
        
        for role in roles:
            role_id = role.role_id
            role_name = db.query(Role.name).filter(Role.id == role_id).first()
            role_names.append(role_name[0])
        
        return role_names
    
    def get_roles_id_from_roles_names(self, db: Session, names: List[str]) -> List[UUID4]:
        return(
        db.query(self.model.id).filter(Role.name.in_(names))
        )
    
    def create_all(self, db:Session):
        exists = db.query(self.model).all()
        if exists:
            return exists
        else:
            db.add_all([
                Role(name="admin"),
                Role(name="applicant")
            ])
            db.commit()
            return db.query(self.model).all()
        
    def create_role(self, db: Session, role_in: RoleCreate) -> Role:
        role = Role(**role_in.dict())
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

role = CRUDRole(Role)
