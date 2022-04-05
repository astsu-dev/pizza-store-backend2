import uuid
from typing import Protocol

from pizza_store.entities.products import Category
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
    ProductCreate,
    ProductCreated,
)


class IProductsServiceRepo(Protocol):
    async def create_category(self, category: CategoryCreate) -> CategoryCreated:
        ...

    async def get_categories(self) -> list[Category]:
        ...

    async def get_category(self, id: uuid.UUID) -> Category:
        ...

    async def delete_category(self, id: uuid.UUID) -> CategoryDeleted:
        ...

    async def create_product(self, product: ProductCreate) -> ProductCreated:
        ...
