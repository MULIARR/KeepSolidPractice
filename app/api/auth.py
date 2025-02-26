from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    hash_password, verify_password,
    create_access_token
)
from app.dto.auth import RegisterRequest, TokenResponse
from constants import Role
from database import db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=TokenResponse, response_class=JSONResponse)
async def register_user(register_data: RegisterRequest):
    """
    reg new user.

    :return: access token
    """

    # 1. hash pass
    hashed = hash_password(register_data.password)

    # 2. db entry
    try:
        user = await db.user.create_user(
            email=register_data.email,
            hashed_password=hashed,
            role=Role.USER
        )
    except IntegrityError:
        # (unique constraint)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    # 3. generate token
    access_token = create_access_token(subject=user.user_id)
    return TokenResponse(access_token=access_token)


@auth_router.post("/token", response_model=TokenResponse, response_class=JSONResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    standard OAuth2 Password Grant Flow:
    """
    email = form_data.username  # username == email
    password = form_data.password

    user = await db.user.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(subject=user.user_id)
    return TokenResponse(access_token=access_token)
