from fastapi import APIRouter
from fastapi.responses import JSONResponse

company_profile_router = APIRouter()

@company_profile_router.get("")
def ping():
    return JSONResponse(content={"success":True,"msg":"Base module installed!"})
