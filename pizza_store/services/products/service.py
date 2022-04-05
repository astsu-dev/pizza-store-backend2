import uuid

from pizza_store.entities.products import Category
from pizza_store.services.products.interfaces import IProductsServiceRepo
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
)


class ProductsService:
    def __init__(self, repo: IProductsServiceRepo) -> None:
        self._repo = repo

    async def create_category(self, category: CategoryCreate) -> CategoryCreated:
        return await self._repo.create_category(category)

    async def get_categories(self) -> list[Category]:
        return await self._repo.get_categories()

    async def get_category(self, id: uuid.UUID) -> Category:
        return await self._repo.get_category(id)

    async def delete_category(self, id: uuid.UUID) -> CategoryDeleted:
        return await self._repo.delete_category(id)
