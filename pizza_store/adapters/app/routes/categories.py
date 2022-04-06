import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pizza_store.adapters.app.dependencies import get_products_service
from pizza_store.services.products.models import CategoryCreate, CategoryUpdate
from pizza_store.services.products.service import ProductsService

router = APIRouter(prefix="/categories")


class CategoryCreatePydantic(BaseModel):
    name: str


class CategoryCreatedPydantic(BaseModel):
    id: uuid.UUID


class CategoryDeletedPydantic(BaseModel):
    id: uuid.UUID


class CategoryUpdatePydantic(BaseModel):
    name: str


class CategoryUpdatedPydantic(BaseModel):
    id: uuid.UUID


class CategoryPydantic(BaseModel):
    id: uuid.UUID
    name: str


@router.get("")
async def get_categories(
    service: ProductsService = Depends(get_products_service),
) -> list[CategoryPydantic]:
    result = await service.get_categories()
    return [CategoryPydantic(id=c.id, name=c.name) for c in result]


@router.post("")
async def create_category(
    category: CategoryCreatePydantic,
    service: ProductsService = Depends(get_products_service),
) -> CategoryCreatedPydantic:
    result = await service.create_category(CategoryCreate(name=category.name))
    return CategoryCreatedPydantic(id=result.id)


@router.get("/{id}")
async def get_category(
    id: uuid.UUID, service: ProductsService = Depends(get_products_service)
) -> CategoryPydantic:
    result = await service.get_category(id)
    return CategoryPydantic(id=result.id, name=result.name)


@router.delete("/{id}")
async def delete_category(
    id: uuid.UUID, service: ProductsService = Depends(get_products_service)
) -> CategoryDeletedPydantic:
    result = await service.delete_category(id)
    return CategoryDeletedPydantic(id=result.id)


@router.put("/{id}")
async def update_category(
    id: uuid.UUID,
    category: CategoryCreatePydantic,
    service: ProductsService = Depends(get_products_service),
) -> CategoryUpdatedPydantic:
    result = await service.update_category(CategoryUpdate(id=id, name=category.name))
    return CategoryUpdatedPydantic(id=result.id)
