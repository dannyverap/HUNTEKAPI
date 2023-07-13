#Python
from datetime import datetime, timedelta

#FastAPI
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
import jwt

#srcUtilities
from src.users.models import User
from src.users.service import CRUDUser
from src.config import settings
from src.auth.config import AuthSettings
from src.auth.utils import generate_access_and_refresh_tokens


@AuthJWT.load_config
def get_config():
    return AuthSettings()


def login(db, authorize, authorization , email, password):
    user = CRUDUser(User).authenticate(db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not CRUDUser(User).is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    # if not user.roles:
    #     role = "traveler"
    # else:
    #     role = user.roles.name
    
    role = "APPLICANT"

    tokens = generate_access_and_refresh_tokens(auth=authorize, user=user, role=role)
    
    return tokens



def refresh(authorize: AuthJWT, db):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    user = CRUDUser(User).get_by_email(db, email=current_user)
    if not user.roles:
        role = "traveler"
    else:
        role = user.roles.name
    claims = {"user_info": {"role": role, "id": str(user.id)}}
    new_access_token = authorize.create_access_token(
        subject=current_user, fresh=False, user_claims=claims)
    return {"access_token": new_access_token}


def login_alternative(db, email, password):
    user = CRUDUser(User).authenticate(db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not CRUDUser(User).is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    if not user.roles:
        role = "traveler"
    else:
        role = user.roles.name

    claims = {"user_info": {"role": role, "id": str(user.id)}}
    claims.update({"sub": user.email})
    claims.update({"exp": datetime.utcnow() + access_token_expires})
    claims.update({"iat": datetime.utcnow()})
    claims.update({"nbf": datetime.utcnow()})
    claims.update({"type": "access"})
    claims.update({"fresh": True})
    access_token = jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    refresh_token = jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return {"access_token": access_token, "refresh_token": refresh_token}
