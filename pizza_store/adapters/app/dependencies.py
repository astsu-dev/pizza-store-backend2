from pizza_store.adapters.db.client import client
from pizza_store.adapters.db.repos.products import ProductsServiceRepo
from pizza_store.services.products.service import ProductsService


def get_products_service() -> ProductsService:
    repo = ProductsServiceRepo(client)
    service = ProductsService(repo)
    return service
