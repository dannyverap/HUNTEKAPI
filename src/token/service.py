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
from src.config import settings
from .models import Token
from .schemas import TokenCreate

# Pydantic
from pydantic import UUID4


class ServiceTokens:
    def get_token_by_user_id(self, db: Session, *, user_id: UUID4) -> Optional[Token]:
        token = db.query(Token).filter_by(user_id=user_id).first()
        return token


    def get_token_by_id(self, db: Session, *, id: UUID4) -> Optional[Token]:
        token = db.query(Token).filter_by(id=id).first()
        return token


    def create_token(self, db: Session, *, order: str, minutes: int, user_id: UUID4) -> int:
        tokenToFind = self.get_token_by_user_id(db=db, user_id=user_id)
        
        code = random.randint(100000, 999999)
        expiration = datetime.utcnow() + timedelta(minutes=minutes)
        
        if tokenToFind:
            if tokenToFind.name == "account_activation":
                tokenToFind.code = code
                tokenToFind.expiration = expiration
                
                db.commit()
                return tokenToFind.code
            else:
                tokenToFind.code = code
                tokenToFind.expiration = expiration
                
                db.commit()
                return tokenToFind.code
        
        new_token = TokenCreate(name=order, code=code, expiration=expiration, user_id=user_id)
        
        db_token = Token(**new_token.dict())
        db.add(db_token)
        db.commit()
        return new_token.code


    def delete_token(self, db: Session, *, token_id: int) -> dict:
        token = db.query(Token).get(token_id)

        if token:
            db.delete(token)
            db.commit()
            return {"message": "Token deleted"}

        return {"message": "Token not found"}
    

token = ServiceTokens()






