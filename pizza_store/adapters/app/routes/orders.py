import uuid

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from pizza_store.adapters.app.dependencies import get_orders_service
from pizza_store.services.orders.models import OrderCreate, OrderItemCreate
from pizza_store.services.orders.service import OrdersService

router = APIRouter(prefix="/orders")


class OrderItemCreatePydantic(BaseModel):
    product_variant_id: uuid.UUID
    amount: PositiveInt


class OrderCreatePydantic(BaseModel):
    phone: str
    items: list[OrderItemCreatePydantic]
    note: str = ""


class OrderCreatedPydantic(BaseModel):
    id: uuid.UUID


@router.post("")
async def create_order(
    order: OrderCreatePydantic, service: OrdersService = Depends(get_orders_service)
) -> OrderCreatedPydantic:
    result = await service.create_order(
        OrderCreate(
            phone=order.phone,
            items=[
                OrderItemCreate(
                    product_variant_id=item.product_variant_id, amount=item.amount
                )
                for item in order.items
            ],
            note=order.note,
        )
    )
    return OrderCreatedPydantic(id=result.id)
