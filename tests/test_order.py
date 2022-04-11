import datetime
import uuid
from decimal import Decimal

from pizza_store.entities.orders import Order, OrderItem
from pizza_store.entities.products import (
    Category,
    ProductVariantWithProduct,
    ProductWithoutVariants,
)


def test_order() -> None:
    order = Order(
        id=uuid.UUID("f7240c84-f12f-4bce-bbe4-76c3105cf6a6"),
        phone="+380991231212",
        address="Baker street 221 B",
        items=[
            OrderItem(
                id=uuid.UUID("48f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                product_variant=ProductVariantWithProduct(
                    id=uuid.UUID("35f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                    name="Small",
                    weight=Decimal(100),
                    weight_units="g",
                    price=Decimal("2.5"),
                    product=ProductWithoutVariants(
                        id=uuid.UUID("2026ab43-1f78-47fd-812e-7570e5b205f3"),
                        name="Margarita",
                        category=Category(
                            id=uuid.UUID("a552c613-8853-4e37-b2d9-05b995fcd26f"),
                            name="Pizzas",
                        ),
                        image_url="https://image.url",
                    ),
                ),
                amount=2,
            )
        ],
        status="UNCOMPLETED",
        note="",
        created_at=datetime.datetime(2022, 3, 2, 19, 15),
    )
    assert order.total_price == Decimal("5")

    order = Order(
        id=uuid.UUID("f7240c84-f12f-4bce-bbe4-76c3105cf6a6"),
        phone="+380991231212",
        address="Baker street 221 B",
        items=[
            OrderItem(
                id=uuid.UUID("48f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                product_variant=ProductVariantWithProduct(
                    id=uuid.UUID("35f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                    name="Small",
                    weight=Decimal(100),
                    weight_units="g",
                    price=Decimal("2.5"),
                    product=ProductWithoutVariants(
                        id=uuid.UUID("2026ab43-1f78-47fd-812e-7570e5b205f3"),
                        name="Margarita",
                        category=Category(
                            id=uuid.UUID("a552c613-8853-4e37-b2d9-05b995fcd26f"),
                            name="Pizzas",
                        ),
                        image_url="https://image.url",
                    ),
                ),
                amount=2,
            ),
            OrderItem(
                id=uuid.UUID("48f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                product_variant=ProductVariantWithProduct(
                    id=uuid.UUID("35f3b5cd-a8b9-441d-aadb-c5bda6498230"),
                    name="Small",
                    weight=Decimal(100),
                    weight_units="g",
                    price=Decimal("3.7"),
                    product=ProductWithoutVariants(
                        id=uuid.UUID("2026ab43-1f78-47fd-812e-7570e5b205f3"),
                        name="Margarita",
                        category=Category(
                            id=uuid.UUID("a552c613-8853-4e37-b2d9-05b995fcd26f"),
                            name="Pizzas",
                        ),
                        image_url="https://image.url",
                    ),
                ),
                amount=1,
            ),
        ],
        status="UNCOMPLETED",
        note="",
        created_at=datetime.datetime(2022, 3, 2, 19, 15),
    )
    assert order.total_price == Decimal("8.7")
