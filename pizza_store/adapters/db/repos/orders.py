import dataclasses
import json

import edgedb

from pizza_store.services.orders.models import OrderCreate, OrderCreated
from pizza_store.utils import UUIDEncoder


class OrdersServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_order(self, order: OrderCreate) -> OrderCreated:
        query = """
        with items := <array<tuple<
            product_variant_id: uuid,
            amount: int16
        >>><json>$items

        insert orders::CustomerOrder {
            phone := <str>$phone,
            items := (
                for item in array_unpack(items)
                union (
                    insert orders::OrderItem {
                        product_variant := (
                            select products::ProductVariant
                            filter .id = item.product_variant_id
                        ),
                        amount := item.amount
                    }
                )
            ),
            note := <str>$note
        };
        """
        items = [dataclasses.asdict(item) for item in order.items]
        result = await self._client.query_single(
            query,
            phone=order.phone,
            items=json.dumps(items, cls=UUIDEncoder),
            note=order.note,
        )
        # TODO: raise error if already exists
        return OrderCreated(id=result.id)
