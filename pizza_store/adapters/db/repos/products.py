import uuid

import edgedb

from pizza_store.entities.products import Category, Product, ProductVariant
from pizza_store.services.products.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductVariantNotFoundError,
)
from pizza_store.services.products.models import (
    CategoryCreate,
    CategoryCreated,
    CategoryDeleted,
    CategoryUpdate,
    CategoryUpdated,
    ProductCreate,
    ProductCreated,
    ProductDeleted,
    ProductUpdate,
    ProductUpdated,
    ProductVariantCreate,
    ProductVariantCreated,
    ProductVariantDeleted,
    ProductVariantUpdate,
    ProductVariantUpdated,
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
        try:
            result = await self._client.query_single(query, name=category.name)
        except edgedb.errors.ConstraintViolationError:
            raise CategoryAlreadyExistsError

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
        if result is None:
            raise CategoryNotFoundError

        return Category(id=result.id, name=result.name)

    async def delete_category(self, id: uuid.UUID) -> CategoryDeleted:
        query = """
        delete products::Category filter .id = <uuid>$id;
        """
        result = await self._client.query_single(query, id=id)
        if result is None:
            raise CategoryNotFoundError

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
        if result is None:
            raise CategoryNotFoundError

        return CategoryUpdated(id=result.id)

    async def create_product(self, product: ProductCreate) -> ProductCreated:
        query = """
        with module products
        insert Product {
            name := <str>$name,
            category := (select Category filter .id = <uuid>$category_id),
            description := <str>$description,
            image_url := <str>$image_url
        };
        """
        try:
            result = await self._client.query_single(
                query,
                name=product.name,
                category_id=product.category_id,
                description=product.description,
                image_url=product.image_url,
            )
        except edgedb.errors.MissingRequiredError as e:
            if "missing value for required link 'category'" in e.get_server_context():
                raise CategoryNotFoundError
            raise
        except edgedb.errors.ConstraintViolationError:
            raise ProductAlreadyExistsError

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
            description,
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
                description=p.description,
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
            description,
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
        if result is None:
            raise ProductNotFoundError

        return Product(
            id=result.id,
            name=result.name,
            category=Category(id=result.category.id, name=result.category.name),
            description=result.description,
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

    async def delete_product(self, id: uuid.UUID) -> ProductDeleted:
        query = """
        delete products::Product
        filter .id = <uuid>$id;
        """
        result = await self._client.query_single(
            query,
            id=id,
        )
        if result is None:
            raise ProductNotFoundError

        return ProductDeleted(id=result.id)

    async def update_product(self, product: ProductUpdate) -> ProductUpdated:
        query = """
        with module products
        update Product
        filter .id = <uuid>$id
        set {
            name := <str>$name,
            category := (select Category filter .id = <uuid>$category_id),
            description := <str>$description,
            image_url := <str>$image_url
        };
        """
        try:
            result = await self._client.query_single(
                query,
                id=product.id,
                name=product.name,
                category_id=product.category_id,
                description=product.description,
                image_url=product.image_url,
            )
        except edgedb.errors.ConstraintViolationError:
            raise ProductAlreadyExistsError
        except edgedb.errors.MissingRequiredError as e:
            if "missing value for required link 'category'" in e.get_server_context():
                raise CategoryNotFoundError
            raise

        return ProductUpdated(id=result.id)

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
        try:
            result = await self._client.query_single(
                query,
                name=product_variant.name,
                weight=product_variant.weight,
                weight_units=product_variant.weight_units,
                price=product_variant.price,
                product_id=product_variant.product_id,
            )
        except edgedb.errors.MissingRequiredError as e:
            if "missing value for required link 'product'" in e.get_server_context():
                raise ProductNotFoundError
            raise

        return ProductVariantCreated(id=result.id)

    async def delete_product_variant(self, id: uuid.UUID) -> ProductVariantDeleted:
        query = """
        delete products::ProductVariant
        filter .id = <uuid>$id;
        """
        result = await self._client.query_single(query, id=id)
        if result is None:
            raise ProductVariantNotFoundError

        return ProductVariantDeleted(id=result.id)

    async def update_product_variant(
        self, product_variant: ProductVariantUpdate
    ) -> ProductVariantUpdated:
        query = """
        update products::ProductVariant
        filter .id = <uuid>$id
        set {
            name := <str>$name,
            weight := <decimal>$weight,
            weight_units := <str>$weight_units,
            price := <decimal>$price
        };
        """
        result = await self._client.query_single(
            query,
            id=product_variant.id,
            name=product_variant.name,
            weight=product_variant.weight,
            weight_units=product_variant.weight_units,
            price=product_variant.price,
        )
        if result is None:
            raise ProductVariantNotFoundError

        return ProductVariantUpdated(id=result.id)
