import os
import uvicorn
from functools import lru_cache
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config import Settings
from src.router import api_router

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Huntek",
    version="0.0.1",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@lru_cache()
def get_settings():
    return Settings()

@app.on_event("shutdown")
def close_db_connection():
    from src.dependencies import get_db
    db = get_db()
    db.close()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

