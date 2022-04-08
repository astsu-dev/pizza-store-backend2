from functools import lru_cache

from pizza_store.adapters.db.client import client
from pizza_store.adapters.db.repos.auth import AuthServiceRepo
from pizza_store.adapters.db.repos.orders import OrdersServiceRepo
from pizza_store.adapters.db.repos.products import ProductsServiceRepo
from pizza_store.services.auth.models import JWTConfig
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
