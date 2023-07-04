from fastapi import Body, Depends, BackgroundTasks, Query
from fastapi import status, HTTPException, APIRouter, Security
from src.dependencies import get_current_active_user, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .service import role as role_service

roles_router = APIRouter()

@roles_router.get("/ping")
def ping():
    return JSONResponse(content={"success":True,"msg":"Pong!"})