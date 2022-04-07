import uuid

from pizza_store.entities.orders import Order, OrderStatus
from pizza_store.services.orders.interfaces import IOrdersServiceRepo
from pizza_store.services.orders.models import (
    OrderCreate,
    OrderCreated,
    OrderUpdate,
    OrderUpdated,
)


class OrdersService:
    def __init__(self, repo: IOrdersServiceRepo) -> None:
        self._repo = repo

    async def create_order(self, order: OrderCreate) -> OrderCreated:
        return await self._repo.create_order(order)

    async def get_orders(self, status: OrderStatus | None = None) -> list[Order]:
        return await self._repo.get_orders(status)

    async def get_order(self, id: uuid.UUID) -> Order:
        return await self._repo.get_order(id)

    async def update_order(self, order: OrderUpdate) -> OrderUpdated:
        return await self._repo.update_order(order)
