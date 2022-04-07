import uuid
from typing import Protocol

from pizza_store.entities.orders import Order, OrderStatus
from pizza_store.services.orders.models import OrderCreate, OrderCreated


class IOrdersServiceRepo(Protocol):
    async def create_order(self, order: OrderCreate) -> OrderCreated:
        ...

    async def get_orders(self, status: OrderStatus | None = None) -> list[Order]:
        ...

    async def get_order(self, id: uuid.UUID) -> Order:
        ...
