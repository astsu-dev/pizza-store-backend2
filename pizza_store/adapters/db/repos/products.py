import edgedb

from pizza_store.entities.products import Category
from pizza_store.services.products.models import CategoryCreate, CategoryCreated


class ProductsServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_category(self, category: CategoryCreate) -> CategoryCreated:
        query = """
        insert products::Category {
            name := <str>$name
        };
        """
        result = await self._client.query(query, name=category.name)
        return CategoryCreated(id=result[0].id)

    async def get_categories(self) -> list[Category]:
        query = """
        select products::Category {
            id,
            name
        };
        """
        result = await self._client.query(query)
        return [Category(id=c.id, name=c.name) for c in result]