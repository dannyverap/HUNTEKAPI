from typing import Optional
from pydantic import BaseModel, UUID4
from fastapi.param_functions import Body

class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    id: UUID4
    role: str = None

class OAuth2PasswordRequestForm:
    def __init__(
        self,
        email: str = Body(...),
        password: str = Body(...),
    ):
        self.email = email
        self.password = password


class ActivationProfile(BaseModel):
    name: str
    first_last_name: str
    second_last_name: str | None = None
    phone: str
    gender: str
    date_of_birth: str


class ActivationPayload(BaseModel):
    token: str
    first : bool | None = None
    password: str | None = None
    profile: ActivationProfile