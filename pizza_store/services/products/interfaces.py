import uuid
from typing import Protocol

from pizza_store.entities.products import Category, Product
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
    ProductCreate,
    ProductCreated,
    ProductVariantCreate,
    ProductVariantCreated,
    ProductVariantDeleted,
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

    async def get_products(self, category_id: uuid.UUID | None = None) -> list[Product]:
        ...

    async def create_product_variant(
        self, product_variant: ProductVariantCreate
    ) -> ProductVariantCreated:
        ...

    async def delete_product_variant(self, id: uuid.UUID) -> ProductVariantDeleted:
        ...
