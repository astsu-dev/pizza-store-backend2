import uuid
from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Literal

from pizza_store.entities.products import ProductVariantWithProduct

OrderStatus = Literal["UNCOMPLETED", "COMPLETED", "CANCELLED"]


@dataclass(frozen=True)
class OrderItem:
    """Ordered product.

    Has function to calculate `amount` * `product_variant.price`.

    Attributes:
        product_variant: variant of product to order.
        amount: amount of product.
    """

    product_variant: ProductVariantWithProduct
    amount: int

    @cached_property
    def total_price(self) -> Decimal:
        return self.product_variant.price * self.amount


@dataclass(frozen=True)
class Order:
    """Customer order data.

    Has function to calculate order total price.

    Attributes:
        id: order id.
        phone: customer phone.
        items: products to order.
        status: order status.
        note: customer note.
    """

    id: uuid.UUID
    phone: str
    items: list[OrderItem]
    status: OrderStatus
    note: str

    @cached_property
    def total_price(self) -> Decimal:
        prices = [i.total_price for i in self.items]
        return sum(prices, Decimal(0))
