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
from sqlalchemy.orm import Session
from src.roles.constants import Role
from src.dependencies import get_current_active_user, get_db
from .service import user as user_service
from .schemas import User, UserCreate, UserUpdate
from src.users.constants import AdditionalClaims
from src.utils.utils import send_new_account_email, send_new_account_email_activation_pwd, send_new_account_email_pwd, send_email, send_reset_password_email, open_html_by_environment
from src.utils.utils import generate_token, verify_token
from src.config import settings
from src.auth.schemas import Token
from src.auth.constants import AdditionalClaims as PasswordClaims
from src.roles.service import role as role_service
from src.token.service import token as tokens_service
from src.auth.utils import generate_access_and_refresh_tokens


users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: User = Security(get_current_active_user,
        #                               scopes=[Role.ADMIN["name"]]),
):
    """
    Retrieve users.
    """
    # if current_user.roles.name == Role.ADMIN["name"]:
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
        first_name: str = Body(...),
        last_name: str = Body(...),
        background_tasks: BackgroundTasks,
) -> Any:
    user = user_service.get_by_email(db, email=email)
    if user:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )
        else: 
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    new_user = UserCreate(email=email, password=password,
                          first_name=first_name, last_name=last_name)
    user = user_service.create(db, user=new_user)
    
    confirmation_code = tokens_service.create_token(db, order="email_activation", minutes=720, user_id=user.id)
    
    send_new_account_email_activation_pwd(email_to=user.email, username=user.first_name, code=confirmation_code, password=password,
                                          background_tasks=background_tasks,  first=True)
    
    db.commit()
    return user


@users_router.put('/newcode', status_code=status.HTTP_200_OK)
def send_new_code(
    request: Request,
    *,
    db: Session = Depends(get_db),
    email: EmailStr = Body(...),
    order: str = Body(...),
    background_tasks: BackgroundTasks,
) -> Any:
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
    new_confirmation_code = tokens_service.create_token(db, order=order, minutes=720, user_id=user.id)
    
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


@users_router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def get_current_user(
        db: Session = Depends(get_db),
        current_user: User = Security(
            get_current_active_user,
            scopes=[
                Role.ADMIN["name"],
                Role.USER["name"]
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
                Role.USER["name"]
            ],
        ),
) -> Any:
    user = user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user


@users_router.post(
    "/account-activation", status_code=status.HTTP_200_OK
)
def activate_accounts(
        *,
        request: Request,
        code: int = Body(...),
        db: Session = Depends(get_db),
        email: EmailStr = Body(...),
        authorize: AuthJWT = Depends(),
) -> Any:
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user does not exist in the system"
        )

    token = tokens_service.get_token_by_user_id(db, user_id=user.id)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid code"
        )
    elif not token.code == int(code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid code",
        )
    elif token.created_at > token.expiration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="code expired",
        )
    elif user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already activated",
        )
        
    user.is_active = True
    tokens_service.delete_token(db, token_id=token.id)
    

    role = "APPLICANT"

    
    tokens = generate_access_and_refresh_tokens(auth=authorize, user=user, role=role)

    db.commit()
    return tokens
    


# --------------------------------------------

# @users_router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
# def create_user(
#         *,
#         db: Session = Depends(get_db),
#         user_in: UserCreate,
# ) -> Any:
#     user = user_service.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="El usuario con este correo electrónico ya existe en el sistema.",
#         )

#     new_user = user_service.create(db, obj_in=user_in)
#     return new_user
