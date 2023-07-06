"""Main API Router for the application"""
from fastapi import APIRouter

from src.utils.router import utils_router
from src.auth.router import auth_router
from src.users.router import users_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(utils_router, prefix="/utils", tags=["Utils"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])