# Python
from pprint import pprint
from typing import Any, Dict, Optional, Union, List
import random
from datetime import timedelta, datetime
from fastapi_jwt_auth import AuthJWT

# SqlAlchemy
from sqlalchemy.orm import Session

# SrcUtilities
from src.auth.utils import get_password_hash, verify_password
from src.config import settings
from .models import Token
from .schemas import TokenCreate
from src.users.service import user as user_service

# Pydantic
from pydantic import UUID4


class ServiceTokens:
    def get_tokens_by_user_id(self, db: Session, *, user_id: UUID4) -> Optional[Token]:
        token = db.query(Token).filter_by(user_id=user_id).all()
        return token


    def get_token_by_id(self, db: Session, *, id: UUID4) -> Optional[Token]:
        token = db.query(Token).filter_by(id=id).first()
        return token
    
    
    def get_token_by_name(self, db: Session, *, user_id: UUID4, name: str) -> Optional[Token]:
        tokenList = self.get_tokens_by_user_id(db=db, user_id=user_id)
        for token in tokenList:
            if token.name == name:
                return token
        return False
            

    def create_token(self, db: Session, *, order: str, minutes: int, user_id: UUID4) -> int:
        tokenList = self.get_tokens_by_user_id(db=db, user_id=user_id)
        
        code = random.randint(100000, 999999)
        expiration = datetime.utcnow() + timedelta(minutes=minutes)
        
        for token in tokenList:
            if token.name == order:
                token.code = code
                token.expiration = expiration
                    
                db.commit()
                return token.code
                
        
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
            return True

        return False
    

token = ServiceTokens()






