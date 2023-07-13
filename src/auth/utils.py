#Python
from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt

#FastAPI
from fastapi_jwt_auth import AuthJWT

#Pydantic
from pydantic import UUID4, EmailStr

#srcUtilities
from src.config import settings
from src.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def create_access_token(
#     subject: Union[str, Any], expires_delta: timedelta = None
# ) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt


def generate_access_and_refresh_tokens(auth: AuthJWT, user: User, role: str) -> dict:
    claims = {"user_info": {
                            "id": str(user.id),
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "role": role,
                            }}
    
    access_token_expires = timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    access_token = auth.create_access_token(
                                            subject=user.email,
                                            fresh=True,
                                            expires_time=access_token_expires,
                                            algorithm=settings.ALGORITHM,
                                            user_claims=claims
                                            )
    refresh_token = auth.create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_email(plain_email: str, hashed_email: str) -> bool:
    return pwd_context.verify(plain_email, hashed_email)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_email_hash(email: EmailStr) -> str:
    return pwd_context.hash(email)
