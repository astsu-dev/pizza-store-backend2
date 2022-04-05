import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryCreate:
    name: str


@dataclass(frozen=True)
class CategoryCreated:
    id: uuid.UUID


CategoryDeleted = CategoryCreated
