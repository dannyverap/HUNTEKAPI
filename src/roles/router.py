from fastapi import Body, Depends, BackgroundTasks, Query
from fastapi import status, HTTPException, APIRouter, Security
from src.dependencies import get_current_active_user, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .service import role as role_service
from .models import Role
from src.roles.schemas import RoleCreate

roles_router = APIRouter()

@roles_router.get("/ping")
def ping():
    return JSONResponse(content={"success":True,"msg":"Pong!"})

@roles_router.post("/roles", status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate = Body(...),  # Cambia los argumentos a un solo argumento de tipo RoleCreate
    db: Session = Depends(get_db),
) -> JSONResponse:
    role = role_service.create_role(db, role_in)  # Pasa el objeto RoleCreate directamente
    return JSONResponse(
        content={"success": True, "message": "Role created successfully"},
        status_code=status.HTTP_201_CREATED,
    )