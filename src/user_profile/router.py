# FastAPI
from fastapi import Body, Depends, BackgroundTasks, Query, Request
from fastapi import status, HTTPException, APIRouter, Security
from fastapi.responses import JSONResponse


# user_profile_router = APIRouter()

# @user_profile_router.get("/user_profile")
# async def get_user_profile(
#     db: Session = Depends(get_db),
#     skip: int = 0,
#     limit: int = 100,
#     ##! current user?
# )
#     :
#     return JSONResponse(content={"success":True,"msg":"Base module installed!"})
