# Python
import os
from pprint import pprint
import emails
import jwt
from datetime import datetime, timedelta
from pathlib import Path, WindowsPath
from typing import Optional, Tuple
from emails.template import JinjaTemplate
import tempfile
import random

# Pydantic
from pydantic import BaseModel, UUID4

# SqlAlchemy
from sqlalchemy.orm import class_mapper

# FastAPI
from fastapi import BackgroundTasks

# Pyjwt
from jwt.exceptions import InvalidTokenError

# srcUtilities
from src.config import settings
from src.roles.constants import Role

def validate_role_name(role_name: str)-> bool:
    return role_name.lower() in [name.lower() for name in Role.VAlLID_ROLE_NAMES]