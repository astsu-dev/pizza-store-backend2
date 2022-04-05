import dataclasses
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pizza_store.adapters.app.dependencies import get_products_service
from pizza_store.services.products.models import CategoryCreate
from pizza_store.services.products.service import ProductsService

router = APIRouter(prefix="/categories")


class CategoryCreatePydantic(BaseModel):
    name: str


class CategoryCreatedPydantic(BaseModel):
    id: uuid.UUID


class CategoryPydantic(BaseModel):
    id: uuid.UUID
    name: str


@router.get("/")
async def get_categories(service: ProductsService = Depends(get_products_service)):
    result = await service.get_categories()
    return [CategoryPydantic(**dataclasses.asdict(c)) for c in result]


@router.post("/")
async def create_category(
    category: CategoryCreatePydantic,
    service: ProductsService = Depends(get_products_service),
):
    result = await service.create_category(CategoryCreate(**category.dict()))
    return CategoryCreatedPydantic(**dataclasses.asdict(result))