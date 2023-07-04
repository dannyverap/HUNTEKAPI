from fastapi import APIRouter
from fastapi.responses import JSONResponse

utils_router = APIRouter()

@utils_router.get("/ping")
def ping():
    return JSONResponse(content={"success":True,"msg":"Pong!"})
