from fastapi import APIRouter
from fastapi.responses import JSONResponse

base_router = APIRouter()

@base_router.get("")
def ping():
    return JSONResponse(content={"success":True,"msg":"Base module installed!"})
