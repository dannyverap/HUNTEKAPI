"""Main API Router for the application"""
from fastapi import APIRouter

from src.utils.router import utils_router
from src.auth.router import auth_router
from src.users.router import users_router
from src.user_profile.router import user_profile_router
from src.roles.router import roles_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(utils_router, prefix="/utils", tags=["Utils"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(user_profile_router, prefix="/profile", tags=["Profile"])
api_router.include_router(roles_router, prefix="/roles", tags=["Roles"])