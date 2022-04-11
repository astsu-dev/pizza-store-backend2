from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.main import BaseModel

from pizza_store.adapters.app.dependencies import get_auth_service
from pizza_store.services.auth.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from pizza_store.services.auth.models import UserCreate, UserLogIn
from pizza_store.services.auth.service import AuthService

router = APIRouter(prefix="/auth")


class UserRegisterPydantic(BaseModel):
    username: str
    password: str


class UserLogInPydantic(BaseModel):
    username: str
    password: str


class TokenPydantic(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


@router.post("/register")
async def register_user(
    user: UserRegisterPydantic,
    service: AuthService = Depends(get_auth_service),
) -> TokenPydantic:
    try:
        token = await service.register_user(
            UserCreate(username=user.username, password=user.password)
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists."
        )
    return TokenPydantic(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )


@router.post("/login")
async def login_user(
    user: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
) -> TokenPydantic:
    try:
        token = await service.login_user(
            UserLogIn(username=user.username, password=user.password)
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    return TokenPydantic(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )
