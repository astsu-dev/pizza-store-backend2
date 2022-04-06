import uuid
from dataclasses import dataclass
from decimal import Decimal

from pizza_store.entities.orders import OrderItem, OrderStatus


@dataclass(frozen=True)
class OrderItemCreate:
    product_variant_id: uuid.UUID
    amount: int


@dataclass(frozen=True)
class OrderCreate:
    """Data for creating order.

    Args:
        phone: customer phone.
        items: list of product variant ids.
        note: note about order.
    """

    phone: str
    items: list[OrderItemCreate]
    note: str


@dataclass(frozen=True)
class OrderCreated:
    id: uuid.UUID


# @dataclass(frozen=True)
# class ServiceOrder:
#     """Order with total price."""

#     id: uuid.UUID
#     phone: str
#     items: list[OrderItem]
#     status: OrderStatus
#     note: str
#     total_price: Decimal
