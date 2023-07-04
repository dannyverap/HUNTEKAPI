from typing import Optional, List

from src.database.base import CRUDBase
from src.roles.models import Role
from src.roles.schemas import RoleCreate, RoleUpdate
from sqlalchemy.orm import Session

from pydantic import UUID4

class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(self.model).filter(Role.name == name).first()
    
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


role = CRUDRole(Role)
