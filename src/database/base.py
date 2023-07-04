# Python
import pytz
import datetime
from typing import Any, Generic, List, Optional, Type, TypeVar

# FastAPI
from fastapi.encoders import jsonable_encoder

# Pydantic
from pydantic import BaseModel
from pydantic import UUID4

# SqlAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# src
from src.database.session import metadata
from src.utils.utils import get_time_zone, object_to_dict

Base: Any = declarative_base(metadata=metadata)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

tz = pytz.timezone(get_time_zone())


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | dict,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if len(obj_data) == 0:
            obj_data = object_to_dict(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def delete_by_deleted_at(self, db: Session, *, id: UUID4) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            obj.deleted_at = datetime.datetime.now(tz)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        return None
