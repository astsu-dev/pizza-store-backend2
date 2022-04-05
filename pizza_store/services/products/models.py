import uuid
from dataclasses import dataclass


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
class ProductCreate:
    name: str
    category_id: uuid.UUID
    image_url: str


@dataclass(frozen=True)
class ProductCreated:
    id: uuid.UUID
