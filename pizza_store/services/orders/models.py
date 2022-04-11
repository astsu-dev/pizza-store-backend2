import uuid
from dataclasses import dataclass

from pizza_store.entities.orders import OrderStatus


@dataclass(frozen=True)
class OrderItemCreate:
    product_variant_id: uuid.UUID
    amount: int


@dataclass(frozen=True)
class OrderCreate:
    """Data for creating order."""

    phone: str
    items: list[OrderItemCreate]
    note: str
    address: str


@dataclass(frozen=True)
class OrderCreated:
    id: uuid.UUID


@dataclass(frozen=True)
class OrderUpdate:
    """Data for updating order."""

    id: uuid.UUID
    phone: str
    items: list[OrderItemCreate]
    status: OrderStatus
    note: str
    address: str


@dataclass(frozen=True)
class OrderUpdated:
    id: uuid.UUID
