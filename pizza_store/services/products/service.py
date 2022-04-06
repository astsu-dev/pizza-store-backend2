import uuid

from pizza_store.entities.products import Category, Product
from pizza_store.services.products.interfaces import IProductsServiceRepo
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
    CategoryUpdate,
    CategoryUpdated,
    ProductCreate,
    ProductCreated,
    ProductUpdate,
    ProductUpdated,
    ProductVariantCreate,
    ProductVariantCreated,
    ProductVariantDeleted,
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

    async def update_category(self, category: CategoryUpdate) -> CategoryUpdated:
        return await self._repo.update_category(category)

    async def create_product(self, product: ProductCreate) -> ProductCreated:
        return await self._repo.create_product(product)

    async def get_products(self, category_id: uuid.UUID | None = None) -> list[Product]:
        return await self._repo.get_products(category_id)

    async def get_product(self, id: uuid.UUID) -> Product:
        return await self._repo.get_product(id)

    async def update_product(self, product: ProductUpdate) -> ProductUpdated:
        return await self._repo.update_product(product)

    async def create_product_variant(
        self, product_variant: ProductVariantCreate
    ) -> ProductVariantCreated:
        return await self._repo.create_product_variant(product_variant)

    async def delete_product_variant(self, id: uuid.UUID) -> ProductVariantDeleted:
        return await self._repo.delete_product_variant(id)
