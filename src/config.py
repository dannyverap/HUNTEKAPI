import os
import secrets
from typing import Any, List, Optional, Union, Tuple, Dict
from pydantic import BaseSettings, PostgresDsn, validator
from pydantic.env_settings import SettingsSourceCallable

env_path = os.path.join(os.getcwd(), ".env")


class Settings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = env_path
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            env_settings: SettingsSourceCallable,
            init_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return init_settings, env_settings, file_secret_settings

    SMTP_TLS: str
    SMTP_PORT: str
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str
    EMAILS_FROM_NAME: str
    EMAILS_ENABLED: str
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: str
    SERVER_HOST: str
    ENVIRONMENT: str
    SECRET_KEY: str
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str, None] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    ALGORITHM: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=f'{values.get("POSTGRES_PASSWORD")}',
            host=f'{values.get("POSTGRES_SERVER")}:{values.get("POSTGRES_PORT")}',
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
