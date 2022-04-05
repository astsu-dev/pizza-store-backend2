import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Category:
    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class ProductVariant:
    id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


@dataclass(frozen=True)
class ProductWithoutVariants:
    id: uuid.UUID
    name: str
    category: Category
    image_url: str


@dataclass(frozen=True)
class Product(ProductWithoutVariants):
    variants: list[ProductVariant]


@dataclass(frozen=True)
class ProductVariantWithProduct(ProductVariant):
    product: Product
