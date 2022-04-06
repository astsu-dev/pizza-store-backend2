from pizza_store.adapters.db.client import client
from pizza_store.adapters.db.repos.orders import OrdersServiceRepo
from pizza_store.adapters.db.repos.products import ProductsServiceRepo
from pizza_store.services.orders.service import OrdersService
from pizza_store.services.products.service import ProductsService


def get_products_service() -> ProductsService:
    repo = ProductsServiceRepo(client)
    service = ProductsService(repo)
    return service


def get_orders_service() -> OrdersService:
    repo = OrdersServiceRepo(client)
    service = OrdersService(repo)
    return service
