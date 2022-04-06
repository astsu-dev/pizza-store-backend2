import uuid

import edgedb

from pizza_store.entities.products import Category, Product, ProductVariant
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
    CategoryUpdate,
    CategoryUpdated,
    ProductCreate,
    ProductCreated,
    ProductVariantCreate,
    ProductVariantCreated,
    ProductVariantDeleted,
)


class ProductsServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_category(self, category: CategoryCreate) -> CategoryCreated:
        query = """
        insert products::Category {
            name := <str>$name
        };
        """
        result = await self._client.query_single(query, name=category.name)
        # TODO: raise error if already exists
        return CategoryCreated(id=result.id)

    async def get_categories(self) -> list[Category]:
        query = """
        select products::Category {
            id,
            name
        };
        """
        result = await self._client.query(query)
        return [Category(id=c.id, name=c.name) for c in result]

    async def get_category(self, id: uuid.UUID) -> Category:
        query = """
        select products::Category {
            id,
            name
        } filter .id = <uuid>$id;
        """
        result = await self._client.query_single(query, id=id)
        # TODO: raise error if not exist
        return Category(id=result.id, name=result.name)

    async def delete_category(self, id: uuid.UUID) -> CategoryDeleted:
        query = """
        delete products::Category filter .id = <uuid>$id;
        """
        result = await self._client.query_single(query, id=id)
        # TODO: raise error if not exist
        return CategoryDeleted(id=result.id)

    async def update_category(self, category: CategoryUpdate) -> CategoryUpdated:
        query = """
        update products::Category
        filter .id = <uuid>$id
        set {
            name := <str>$name
        };
        """
        result = await self._client.query_single(
            query, id=category.id, name=category.name
        )
        # TODO: raise error if not exists
        return CategoryUpdated(id=result.id)

    async def create_product(self, product: ProductCreate) -> ProductCreated:
        query = """
        with module products
        insert Product {
            name := <str>$name,
            category := (select Category filter .id = <uuid>$category_id),
            image_url := <str>$image_url
        };
        """
        result = await self._client.query_single(
            query,
            name=product.name,
            category_id=product.category_id,
            image_url=product.image_url,
        )
        # TODO: raise error if already exists
        return ProductCreated(id=result.id)

    async def get_products(self, category_id: uuid.UUID | None = None) -> list[Product]:
        query = """
        select products::Product {
            id,
            name,
            category: {
                id,
                name
            },
            variants: {
                id,
                name,
                weight,
                weight_units,
                price
            },
            image_url
        }
        """
        if category_id is not None:
            query = f"{query} filter .category.id = <uuid>$category_id;"
            result = await self._client.query(query, category_id=category_id)
        else:
            query = f"{query};"
            result = await self._client.query(query)

        return [
            Product(
                id=p.id,
                name=p.name,
                category=Category(id=p.category.id, name=p.category.name),
                image_url=p.image_url,
                variants=[
                    ProductVariant(
                        id=v.id,
                        name=v.name,
                        weight=v.weight,
                        weight_units=v.weight_units,
                        price=v.price,
                    )
                    for v in p.variants
                ],
            )
            for p in result
        ]

    async def get_product(self, id: uuid.UUID) -> Product:
        query = """
        select products::Product {
            id,
            name,
            category: {
                id,
                name
            },
            variants: {
                id,
                name,
                weight,
                weight_units,
                price
            },
            image_url
        } filter .id = <uuid>$id;
        """

        result = await self._client.query_single(query, id=id)
        # TODO: raise error if not exists
        return Product(
            id=result.id,
            name=result.name,
            category=Category(id=result.category.id, name=result.category.name),
            image_url=result.image_url,
            variants=[
                ProductVariant(
                    id=v.id,
                    name=v.name,
                    weight=v.weight,
                    weight_units=v.weight_units,
                    price=v.price,
                )
                for v in result.variants
            ],
        )

    async def create_product_variant(
        self, product_variant: ProductVariantCreate
    ) -> ProductVariantCreated:
        query = """
        with module products
        insert ProductVariant {
            name := <str>$name,
            weight := <decimal>$weight,
            weight_units := <str>$weight_units,
            price := <decimal>$price,
            product := (select Product filter .id = <uuid>$product_id)
        };
        """
        result = await self._client.query_single(
            query,
            name=product_variant.name,
            weight=product_variant.weight,
            weight_units=product_variant.weight_units,
            price=product_variant.price,
            product_id=product_variant.product_id,
        )
        # TODO: raise error if already exists
        return ProductVariantCreated(id=result.id)

    async def delete_product_variant(self, id: uuid.UUID) -> ProductVariantDeleted:
        query = """
        delete products::ProductVariant
        filter .id = <uuid>$id;
        """
        result = await self._client.query_single(query, id=id)
        # TODO: raise error if not exists
        return ProductVariantDeleted(id=result.id)
