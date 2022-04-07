import dataclasses
import json
import uuid
from typing import cast

import edgedb

from pizza_store.entities.orders import Order, OrderItem, OrderStatus
from pizza_store.entities.products import (
    Category,
    ProductVariantWithProduct,
    ProductWithoutVariants,
)
from pizza_store.services.orders.models import OrderCreate, OrderCreated
from pizza_store.utils import UUIDEncoder


class OrdersServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_order(self, order: OrderCreate) -> OrderCreated:
        client = self._client

        create_order_query = """
        insert orders::CustomerOrder {
            phone := <str>$phone,
            note := <str>$note
        };
        """
        create_order_items_query = """
        with items := <array<tuple<
            product_variant_id: uuid,
            amount: int16
        >>><json>$items

        for item in array_unpack(items)
        union (
            insert orders::OrderItem {
                product_variant := (
                    select products::ProductVariant
                    filter .id = item.product_variant_id
                ),
                amount := item.amount,
                customer_order := (
                    select orders::CustomerOrder
                    filter .id = <uuid>$order_id
                )
            }
        );
        """

        items = [dataclasses.asdict(item) for item in order.items]

        async for tx in client.transaction():
            async with tx:
                order_result = await tx.query_single(
                    create_order_query,
                    phone=order.phone,
                    note=order.note,
                )
                order_id = order_result.id
                await tx.query(
                    create_order_items_query,
                    order_id=order_id,
                    items=json.dumps(items, cls=UUIDEncoder),
                )
                # TODO: raise error if already exists
                return OrderCreated(id=order_id)
        assert False, "Unreachable"

    async def get_orders(self, status: OrderStatus | None = None) -> list[Order]:
        query = """
        select orders::CustomerOrder {
            id,
            phone,
            status,
            note,
            created_at,
            items: {
                id,
                product_variant: {
                    id,
                    name,
                    weight,
                    weight_units,
                    price,
                    product: {
                        id,
                        name,
                        category: {
                            id,
                            name
                        },
                        image_url
                    }
                },
                amount
            }
        }
        """
        if status is not None:
            query = f"{query} filter .status = <orders::OrderStatus>$status;"
            result = await self._client.query(query, status=status)
        else:
            query += ";"
            result = await self._client.query(query)

        return [
            Order(
                id=o.id,
                phone=o.phone,
                status=cast(OrderStatus, str(o.status)),
                note=o.note,
                created_at=o.created_at,
                items=[
                    OrderItem(
                        id=oi.id,
                        product_variant=ProductVariantWithProduct(
                            id=oi.product_variant.id,
                            name=oi.product_variant.name,
                            weight=oi.product_variant.weight,
                            weight_units=oi.product_variant.weight_units,
                            price=oi.product_variant.price,
                            product=ProductWithoutVariants(
                                id=oi.product_variant.product.id,
                                name=oi.product_variant.product.name,
                                category=Category(
                                    id=oi.product_variant.product.category.id,
                                    name=oi.product_variant.product.category.name,
                                ),
                                image_url=oi.product_variant.product.image_url,
                            ),
                        ),
                        amount=oi.amount,
                    )
                    for oi in o.items
                ],
            )
            for o in result
        ]

    async def get_order(self, id: uuid.UUID) -> Order:
        query = """
        select orders::CustomerOrder {
            id,
            phone,
            status,
            note,
            created_at,
            items: {
                id,
                product_variant: {
                    id,
                    name,
                    weight,
                    weight_units,
                    price,
                    product: {
                        id,
                        name,
                        category: {
                            id,
                            name
                        },
                        image_url
                    }
                },
                amount
            },
        } filter .id = <uuid>$id;
        """
        o = await self._client.query_single(query, id=id)
        # TODO: raise error if not exists
        return Order(
            id=o.id,
            phone=o.phone,
            status=cast(OrderStatus, str(o.status)),
            note=o.note,
            created_at=o.created_at,
            items=[
                OrderItem(
                    id=oi.id,
                    product_variant=ProductVariantWithProduct(
                        id=oi.product_variant.id,
                        name=oi.product_variant.name,
                        weight=oi.product_variant.weight,
                        weight_units=oi.product_variant.weight_units,
                        price=oi.product_variant.price,
                        product=ProductWithoutVariants(
                            id=oi.product_variant.product.id,
                            name=oi.product_variant.product.name,
                            category=Category(
                                id=oi.product_variant.product.category.id,
                                name=oi.product_variant.product.category.name,
                            ),
                            image_url=oi.product_variant.product.image_url,
                        ),
                    ),
                    amount=oi.amount,
                )
                for oi in o.items
            ],
        )
