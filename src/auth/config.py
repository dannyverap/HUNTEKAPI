from src.config import settings
from pydantic import BaseModel

class AuthSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET_KEY