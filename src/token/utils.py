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
from src.token.constants import Order

def validate_order_name(order: str)-> bool:
    return order.lower() in [name.lower() for name in Order.VAlLID_ORDER_NAMES]