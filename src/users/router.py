# Python
from datetime import timedelta
import secrets
import string
from typing import Any, List
from fastapi_jwt_auth import AuthJWT

# FastAPI
from fastapi import Body, Depends, BackgroundTasks, Query, Request
from fastapi import status, HTTPException, APIRouter, Security
from fastapi.responses import JSONResponse

# Pydantic
from pydantic.networks import EmailStr
from pydantic import UUID4
from sqlalchemy.orm import Session
from src.roles.constants import Role
from src.dependencies import get_current_active_user, get_db
from .service import user as user_service
# , PlannerUser, ManagerUser, PlannerTravelers, ApproverUsers
from .schemas import User, UserCreate, UserUpdate
from src.users.constants import AdditionalClaims
from src.utils.utils import send_new_account_email, send_new_account_email_activation_pwd, send_new_account_email_pwd, send_email, open_html_by_environment
from src.utils.utils import generate_token, verify_token
from src.config import settings
from src.auth.schemas import Token
from src.auth.constants import AdditionalClaims as PasswordClaims
from src.roles.service import role as role_service

users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
def read_users(

        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Security(get_current_active_user,
                                      scopes=[Role.ADMIN["name"]]),
):
    """
    Retrieve users.
    """
    if current_user.roles.name == Role.ADMIN["name"]:
        users = user_service.get_multi(db, skip=skip, limit=limit)
    return users


@users_router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED,
                   response_model_exclude_none=True)
async def create_user(
        request: Request,
        *,
        db: Session = Depends(get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        firstName: str = Body(...),
        lastName: str = Body(...),
        background_tasks: BackgroundTasks,
) -> Any:
    user = user_service.get_by_email(db, email=email)
    if user:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user_in = UserCreate(email=email, password=password,
                         firstName=firstName, lastName=lastName)
    user = user_service.create(db, obj_in=user_in)

    password_reset_token = generate_token(user.email, AdditionalClaims.ACTIVATE_ACCOUNT_PASSWORD["name"], {})
    send_new_account_email_activation_pwd(password=password, email_to=user.email, token=password_reset_token,
                                           background_tasks=background_tasks, username=user.email, first=True)
    db.commit()
    return user


@users_router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def get_current_user(
        db: Session = Depends(get_db),
        current_user: User = Security(
            get_current_active_user,
            scopes=[
                Role.ADMIN["name"],
                Role.APPLICANT["name"]
            ],
        ),
) -> Any:
    user = User.from_orm(current_user)
    return user


@users_router.get("/users/{user_id}", response_model=User)
def read_user_by_id(
        user_id: UUID4,
        current_user: User = Security(
            get_current_active_user,
            scopes=[Role.ADMIN["name"]],
        ),
        db: Session = Depends(get_db),
) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.put("/users/{user_id}", response_model=User)
def update_user_by_id(
        *,
        db: Session = Depends(get_db),
        user_id: UUID4,
        user_in: UserUpdate,
        current_user: User = Security(
            get_current_active_user,
            scopes=[Role.ADMIN["name"]],
        ),
) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_service.update(db, db_obj=user, obj_in=user_in)
    return user


@users_router.put("/users/me", response_model=User)
def update_current_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserUpdate,
        current_user: User = Security(
            get_current_active_user,
            scopes=[
                Role.ADMIN["name"],
                Role.APPLICANT["name"]
            ],
        ),
) -> Any:
    user = user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user


@users_router.post(
    "/account-activation", response_model=Token, status_code=status.HTTP_200_OK
)
def activate_accounts(
        *,
        db: Session = Depends(get_db),
        token: str = Query(...),
        auth: AuthJWT = Depends(),
) -> Any:
    action = [
        AdditionalClaims.ACCOUNT_ACTIVATION_ADMIN["name"],
        AdditionalClaims.ACCOUNT_ACTIVATION_USER["name"],
    ]
    email, token = verify_token(token, action)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    elif user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already activated",
        )
    user.is_active = True
    db.commit()
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {"user_info": {"role": user.roles.name, "id": str(user.id)}}
    access_token = auth.create_access_token(subject=user.email,
                                            fresh=True,
                                            expires_time=access_token_expires,
                                            user_claims=claims,
                                            algorithm="HS256")
    refresh_token = auth.create_refresh_token(subject=user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)
