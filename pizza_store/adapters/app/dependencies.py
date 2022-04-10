from functools import lru_cache
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from pizza_store.adapters.db.client import client
from pizza_store.adapters.db.repos.auth import AuthServiceRepo
from pizza_store.adapters.db.repos.orders import OrdersServiceRepo
from pizza_store.adapters.db.repos.products import ProductsServiceRepo
from pizza_store.services.auth.exceptions import (
    AccessForbiddenError,
    InvalidAccessToken,
)
from pizza_store.services.auth.models import JWTConfig, UserTokenData
from pizza_store.services.auth.service import AuthService
from pizza_store.services.orders.service import OrdersService
from pizza_store.services.products.service import ProductsService
from pizza_store.settings import settings


@lru_cache
def get_products_service() -> ProductsService:
    repo = ProductsServiceRepo(client)
    service = ProductsService(repo)
    return service


@lru_cache
def get_orders_service() -> OrdersService:
    repo = OrdersServiceRepo(client)
    service = OrdersService(repo)
    return service


@lru_cache
def get_auth_service() -> AuthService:
    repo = AuthServiceRepo(client)
    jwt_config = JWTConfig(
        algorithm=settings.jwt_algorithm,
        secret=settings.jwt_secret,
        expires_in=settings.jwt_expires_in,
    )
    service = AuthService(repo, jwt_config)
    return service


def get_current_user(
    is_admin_required: bool,
) -> Callable[[str, AuthService], UserTokenData]:
    def dependency(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login")),
        service: AuthService = Depends(get_auth_service),
    ) -> UserTokenData:
        try:
            return service.get_user_from_token(token, is_admin_required)
        except InvalidAccessToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
            )
        except AccessForbiddenError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions."
            )

    return dependency
