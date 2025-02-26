import os
from enum import StrEnum


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"
