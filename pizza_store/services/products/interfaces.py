from typing import Protocol
import uuid

from pizza_store.entities.products import Category
from pizza_store.services.products.models import CategoryCreate, CategoryCreated


class IProductsServiceRepo(Protocol):
    async def create_category(self, category: CategoryCreate) -> CategoryCreated:
        ...

    async def get_categories(self) -> list[Category]:
        ...

    async def get_category(self, id: uuid.UUID) -> Category:
        ...
