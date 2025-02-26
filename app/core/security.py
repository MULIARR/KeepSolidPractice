import hashlib
import hmac
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from database import db
from database.schema import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def hash_password(password: str, salt: str = "") -> str:
    salted = password + salt  # TODO: [low priority] every user must have his own salt
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str, salt: str = "") -> bool:
    return hmac.compare_digest(
        hash_password(plain_password, salt),
        hashed_password
    )


def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:
    """
    JWT-token generation, где subject — user_id.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    get user_id from token, then get from db
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = await db.user.get_user_by_id(user_id)
    if not user:
        raise credentials_exception

    return user
