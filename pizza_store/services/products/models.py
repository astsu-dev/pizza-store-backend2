import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CategoryCreate:
    name: str


@dataclass(frozen=True)
class CategoryCreated:
    id: uuid.UUID


@dataclass(frozen=True)
class CategoryDeleted:
    id: uuid.UUID


@dataclass(frozen=True)
class CategoryUpdate:
    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class CategoryUpdated:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductCreate:
    name: str
    category_id: uuid.UUID
    image_url: str


@dataclass(frozen=True)
class ProductCreated:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductDeleted:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductUpdate:
    id: uuid.UUID
    name: str
    category_id: uuid.UUID
    image_url: str


@dataclass(frozen=True)
class ProductUpdated:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductVariantCreate:
    product_id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


@dataclass(frozen=True)
class ProductVariantCreated:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductVariantUpdate:
    id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


@dataclass(frozen=True)
class ProductVariantUpdated:
    id: uuid.UUID


@dataclass(frozen=True)
class ProductVariantDeleted:
    id: uuid.UUID
