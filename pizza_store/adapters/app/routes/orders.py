import uuid
from decimal import Decimal

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from pizza_store.adapters.app.dependencies import get_orders_service
from pizza_store.adapters.app.routes.categories import CategoryPydantic
from pizza_store.adapters.app.routes.product_variants import (
    ProductVariantWithProductPydantic,
    ProductWithoutVariantsPydantic,
)
from pizza_store.entities.orders import OrderStatus
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


class OrderItemPydantic(BaseModel):
    product_variant: ProductVariantWithProductPydantic
    amount: int
    total_price: Decimal


class OrderPydantic(BaseModel):
    id: uuid.UUID
    phone: str
    items: list[OrderItemPydantic]
    status: OrderStatus
    note: str
    total_price: Decimal


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


@router.get("")
async def get_orders(
    status: OrderStatus | None = None,
    service: OrdersService = Depends(get_orders_service),
) -> list[OrderPydantic]:
    result = await service.get_orders(status)
    return [
        OrderPydantic(
            id=o.id,
            phone=o.phone,
            status=o.status,
            items=[
                OrderItemPydantic(
                    product_variant=ProductVariantWithProductPydantic(
                        id=oi.product_variant.id,
                        name=oi.product_variant.name,
                        weight=oi.product_variant.weight,
                        weight_units=oi.product_variant.weight_units,
                        price=oi.product_variant.price,
                        product=ProductWithoutVariantsPydantic(
                            id=oi.product_variant.product.id,
                            name=oi.product_variant.product.name,
                            category=CategoryPydantic(
                                id=oi.product_variant.product.category.id,
                                name=oi.product_variant.product.category.name,
                            ),
                            image_url=oi.product_variant.product.image_url,
                        ),
                    ),
                    amount=oi.amount,
                    total_price=oi.total_price,
                )
                for oi in o.items
            ],
            note=o.note,
            total_price=o.total_price,
        )
        for o in result
    ]


@router.get("/{id}")
async def get_order(
    id: uuid.UUID,
    service: OrdersService = Depends(get_orders_service),
) -> OrderPydantic:
    o = await service.get_order(id)
    return OrderPydantic(
        id=o.id,
        phone=o.phone,
        status=o.status,
        items=[
            OrderItemPydantic(
                product_variant=ProductVariantWithProductPydantic(
                    id=oi.product_variant.id,
                    name=oi.product_variant.name,
                    weight=oi.product_variant.weight,
                    weight_units=oi.product_variant.weight_units,
                    price=oi.product_variant.price,
                    product=ProductWithoutVariantsPydantic(
                        id=oi.product_variant.product.id,
                        name=oi.product_variant.product.name,
                        category=CategoryPydantic(
                            id=oi.product_variant.product.category.id,
                            name=oi.product_variant.product.category.name,
                        ),
                        image_url=oi.product_variant.product.image_url,
                    ),
                ),
                amount=oi.amount,
                total_price=oi.total_price,
            )
            for oi in o.items
        ],
        note=o.note,
        total_price=o.total_price,
    )
