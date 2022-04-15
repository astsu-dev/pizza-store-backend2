import datetime
import uuid
from decimal import Decimal

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from pydantic.types import PositiveInt
from starlette import status

from pizza_store.adapters.app.dependencies import get_current_user, get_orders_service
from pizza_store.adapters.app.routes.categories import CategoryPydantic
from pizza_store.adapters.app.routes.product_variants import (
    ProductVariantWithProductPydantic,
    ProductWithoutVariantsPydantic,
)
from pizza_store.entities.orders import OrderStatus
from pizza_store.services.auth.models import UserTokenData
from pizza_store.services.orders.exceptions import OrderNotFoundError
from pizza_store.services.orders.models import OrderCreate, OrderItemCreate, OrderUpdate
from pizza_store.services.orders.service import OrdersService
from pizza_store.services.products.exceptions import ProductVariantNotFoundError

router = APIRouter(prefix="/orders")


class OrderItemCreatePydantic(BaseModel):
    product_variant_id: uuid.UUID
    amount: PositiveInt


class OrderCreatePydantic(BaseModel):
    phone: str
    items: list[OrderItemCreatePydantic]
    address: str
    note: str = ""


class OrderCreatedPydantic(BaseModel):
    id: uuid.UUID


class OrderItemPydantic(BaseModel):
    id: uuid.UUID
    product_variant: ProductVariantWithProductPydantic
    amount: PositiveInt
    total_price: Decimal


class OrderUpdatePydantic(BaseModel):
    phone: str
    items: list[OrderItemCreatePydantic]
    status: OrderStatus
    note: str
    address: str


class OrderUpdatedPydantic(BaseModel):
    id: uuid.UUID


class OrderPydantic(BaseModel):
    id: uuid.UUID
    phone: str
    items: list[OrderItemPydantic]
    status: OrderStatus
    note: str
    address: str
    total_price: Decimal
    created_at: datetime.datetime


@router.post("")
async def create_order(
    order: OrderCreatePydantic,
    service: OrdersService = Depends(get_orders_service),
) -> OrderCreatedPydantic:
    try:
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
                address=order.address,
            )
        )
    except ProductVariantNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant does not exist.",
        )
    return OrderCreatedPydantic(id=result.id)


@router.get("")
async def get_orders(
    status: OrderStatus | None = None,
    service: OrdersService = Depends(get_orders_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> list[OrderPydantic]:
    result = await service.get_orders(status)
    return [
        OrderPydantic(
            id=o.id,
            phone=o.phone,
            status=o.status,
            note=o.note,
            address=o.address,
            total_price=o.total_price,
            created_at=o.created_at,
            items=[
                OrderItemPydantic(
                    id=oi.id,
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
                            description=oi.product_variant.product.description,
                            image_url=oi.product_variant.product.image_url,
                        ),
                    ),
                    amount=oi.amount,
                    total_price=oi.total_price,
                )
                for oi in o.items
            ],
        )
        for o in result
    ]


@router.get("/{id}")
async def get_order(
    id: uuid.UUID,
    service: OrdersService = Depends(get_orders_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> OrderPydantic:
    try:
        o = await service.get_order(id)
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order does not exist."
        )
    return OrderPydantic(
        id=o.id,
        phone=o.phone,
        status=o.status,
        note=o.note,
        address=o.address,
        total_price=o.total_price,
        created_at=o.created_at,
        items=[
            OrderItemPydantic(
                id=oi.id,
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
                        description=oi.product_variant.product.description,
                        image_url=oi.product_variant.product.image_url,
                    ),
                ),
                amount=oi.amount,
                total_price=oi.total_price,
            )
            for oi in o.items
        ],
    )


@router.put("/{id}")
async def update_order(
    id: uuid.UUID,
    order: OrderUpdatePydantic,
    service: OrdersService = Depends(get_orders_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> OrderUpdatedPydantic:
    try:
        result = await service.update_order(
            OrderUpdate(
                id=id,
                phone=order.phone,
                status=order.status,
                note=order.note,
                address=order.address,
                items=[
                    OrderItemCreate(
                        product_variant_id=item.product_variant_id, amount=item.amount
                    )
                    for item in order.items
                ],
            )
        )
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order does not exist."
        )
    except ProductVariantNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant does not exist.",
        )

    return OrderUpdatedPydantic(id=result.id)
