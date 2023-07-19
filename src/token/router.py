# Python
from datetime import timedelta, datetime
import secrets
import string
from typing import Any, List
from fastapi_jwt_auth import AuthJWT
import json


# FastAPI
from fastapi import Body, Depends, BackgroundTasks, Query, Request
from fastapi import status, HTTPException, APIRouter, Security
from fastapi.responses import JSONResponse
from fastapi import Header, Response

# Pydantic
from pydantic.networks import EmailStr
from pydantic import UUID4

# SqlAlchemy
from sqlalchemy.orm import Session

# SrcUtilities
from src.roles.constants import Role
from src.dependencies import get_current_active_user, get_db
from src.users.service import user as user_service
from src.users.schemas import User, UserCreate, UserUpdate
from src.users.constants import AdditionalClaims
from src.utils.utils import send_new_account_email, send_new_account_email_activation_pwd, send_new_account_email_pwd, send_email, send_reset_password_email, open_html_by_environment
from src.utils.utils import generate_token, verify_token
from src.config import settings
from src.auth.schemas import Token
from src.auth.constants import AdditionalClaims as PasswordClaims
from src.roles.service import role as role_service
from src.token.service import token as tokens_service
from src.auth.utils import generate_access_and_refresh_tokens
from src.roles.utils import validate_role_name
from src.token.utils import validate_order_name


tokens_router = APIRouter()


@tokens_router.post('/newcode', status_code=status.HTTP_200_OK)
def send_new_code(
    request: Request,
    *,
    db: Session = Depends(get_db),
    email: EmailStr = Body(...),
    order: str = Body(...),
    background_tasks: BackgroundTasks,
) -> Any:
    is_valid_order = validate_order_name(order=order)
    if not is_valid_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order name"
        )
    
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user does not exist in the system",
        )
    if user.is_active and order == "account_activation":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already active"
        )
    new_confirmation_code = tokens_service.create_token(db, order=order.lower(), minutes=720, user_id=user.id)
    
    send_new_account_email_activation_pwd(
        password=user.password,
        email_to=user.email,
        code=new_confirmation_code,
        background_tasks=background_tasks,
        username=user.first_name,
        first=True
    )
    
    db.commit()
    return {"message": "New verification code sent successfully."}
