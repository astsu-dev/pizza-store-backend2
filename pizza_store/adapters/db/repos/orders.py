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
from pizza_store.services.orders.exceptions import OrderNotFoundError
from pizza_store.services.orders.models import (
    OrderCreate,
    OrderCreated,
    OrderUpdate,
    OrderUpdated,
)
from pizza_store.services.products.exceptions import ProductVariantNotFoundError
from pizza_store.utils import UUIDEncoder


class OrdersServiceRepo:
    def __init__(self, client: edgedb.asyncio_client.AsyncIOClient) -> None:
        self._client = client

    async def create_order(self, order: OrderCreate) -> OrderCreated:
        client = self._client

        create_order_query = """
        insert orders::CustomerOrder {
            phone := <str>$phone,
            note := <str>$note,
            address := <str>$address
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
                    address=order.address,
                )
                order_id = order_result.id
                try:
                    await tx.query(
                        create_order_items_query,
                        order_id=order_id,
                        items=json.dumps(items, cls=UUIDEncoder),
                    )
                except edgedb.errors.MissingRequiredError as e:
                    if (
                        "missing value for required link 'product_variant'"
                        in e.get_server_context()
                    ):
                        raise ProductVariantNotFoundError
                    raise
                return OrderCreated(id=order_id)
        assert False, "Unreachable"

    async def get_orders(self, status: OrderStatus | None = None) -> list[Order]:
        query = """
        select orders::CustomerOrder {
            id,
            phone,
            status,
            note,
            address,
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
                        description,
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
                address=o.address,
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
                                description=oi.product_variant.product.description,
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
            address,
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
                        description,
                        image_url
                    }
                },
                amount
            },
        } filter .id = <uuid>$id;
        """
        o = await self._client.query_single(query, id=id)
        if o is None:
            raise OrderNotFoundError

        return Order(
            id=o.id,
            phone=o.phone,
            status=cast(OrderStatus, str(o.status)),
            note=o.note,
            address=o.address,
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
                            description=oi.product_variant.product.description,
                            image_url=oi.product_variant.product.image_url,
                        ),
                    ),
                    amount=oi.amount,
                )
                for oi in o.items
            ],
        )

    async def update_order(self, order: OrderUpdate) -> OrderUpdated:
        delete_old_order_items_query = """
        delete orders::OrderItem
        filter .customer_order.id = <uuid>$order_id;
        """
        update_order_query = """
        update orders::CustomerOrder
        filter .id = <uuid>$id
        set {
            phone := <str>$phone,
            status := <orders::OrderStatus>$status,
            note := <str>$note,
            address := <str>$address
        };
        """
        create_new_order_items_query = """
        with items := <array<tuple<
            product_variant_id: uuid,
            amount: int16
        >>><json>$items
        for item in array_unpack(items) union (
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

        async for tx in self._client.transaction():
            async with tx:
                order_id = order.id
                items = [dataclasses.asdict(item) for item in order.items]
                items_json = json.dumps(items, cls=UUIDEncoder)

                # Delete old order items
                await tx.query(delete_old_order_items_query, order_id=order_id)
                # Update order
                result = await tx.query_single(
                    update_order_query,
                    id=order_id,
                    phone=order.phone,
                    status=order.status,
                    note=order.note,
                    address=order.address,
                )
                if result is None:
                    raise OrderNotFoundError
                # Create new order items
                try:
                    await tx.query(
                        create_new_order_items_query,
                        order_id=order_id,
                        items=items_json,
                    )
                except edgedb.errors.MissingRequiredError as e:
                    if (
                        "missing value for required link 'product_variant'"
                        in e.get_server_context()
                    ):
                        raise ProductVariantNotFoundError
                    raise

                return OrderUpdated(id=order_id)
        assert False, "Unreachable"
