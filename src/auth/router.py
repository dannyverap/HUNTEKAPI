from datetime import timedelta
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Depends, HTTPException, Security, BackgroundTasks
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm as OAuth2PasswordBearer_2
from src.config import settings

from .utils import get_password_hash
from .constants import AdditionalClaims

from .schemas import ActivationPayload, Token, OAuth2PasswordRequestForm
from .service import login as login_service, login_alternative
from .service import refresh as refresh_service
from src.dependencies import get_db
from src.users.service import user as user_service
from src.utils.utils import generate_token, send_reset_password_email, verify_token

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    authorize: AuthJWT = Depends(),
) -> Any:
    """
    Authentication to get access token and refresh token
    - Params:
        - **email**: each user must have a unique email
        - **password**: min length 12 symbols
    - return:
        - **access_token**
        - **refresh_token**
    """
    return login_service(db, authorize, form_data.email, form_data.password)


@auth_router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordBearer_2 = Depends(),
) -> Any:
    """
    Authentication to get access token
    - Params:
        - **email**: each user must have a unique email
        - **password**: min length 12 symbols
    - return:
        - **access_token**
    """
    return login_alternative(db, form_data.username, form_data.password)


@auth_router.post("/refresh")
def refresh(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> Any:
    """
    Refresh token endpoint. This will generate a new access token from
    the refresh token
    - Authorization:
        - **Bearer refresh_token**
    - return:
        - **access_token**
    """
    return refresh_service(authorize, db)


@auth_router.post("/login/test-token")
def test_token():
    return JSONResponse(content={"success": True, "msg": "Test Token"})


@auth_router.get("/password/recovery/{email}")
def password_recovery(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    password_reset_token = generate_token(
        email, AdditionalClaims.RESET_PASSWORD["name"]
    )
    send_reset_password_email(email_to=user.email, username=user.first_name,
                              token=password_reset_token, background_tasks=background_tasks)
    return JSONResponse(content={"success": True, "msg": "Password Recovery Sent"})


@auth_router.post("/password/reset")
def password_reset(token: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    action = AdditionalClaims.RESET_PASSWORD["name"]
    email, action = verify_token(token, action)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid Token")
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = get_password_hash(password)
    user.password = hashed_password
    db.commit()
    return JSONResponse(content={"success": True, "msg": "Password Reset"})


@auth_router.post("/password/activation")
def password_activation(activation: ActivationPayload, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    action = [AdditionalClaims.ACTIVATE_ACCOUNT_PASSWORD["name"]]
    email, action = verify_token(activation.token, action)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid Token")
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not activation.first:
        hashed_password = get_password_hash(activation.password)
        user.hashed_password = hashed_password
    user.is_active = True
    user.profile.name = activation.profile.name
    user.profile.first_last_name = activation.profile.first_last_name
    user.profile.second_last_name = activation.profile.second_last_name or None
    user.profile.phone = activation.profile.phone
    user.profile.gender = activation.profile.gender
    user.profile.date_of_birth = activation.profile.date_of_birth
    db.commit()
    if activation.first:
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        claims = {"user_info": {"role": user.roles.name, "id": str(user.id)}}
        access_token = authorize.create_access_token(subject=user.email,
                                                     fresh=True,
                                                     expires_time=access_token_expires,
                                                     user_claims=claims,
                                                     algorithm="HS256")
        refresh_token = authorize.create_refresh_token(subject=user.email)
        return Token(access_token=access_token, refresh_token=refresh_token)
    return login_service(db, authorize, email, activation.password)
