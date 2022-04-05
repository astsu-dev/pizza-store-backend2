import dataclasses
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.networks import HttpUrl

from pizza_store.adapters.app.dependencies import get_products_service
from pizza_store.services.products.models import ProductCreate
from pizza_store.services.products.service import ProductsService

router = APIRouter(prefix="/products")


class ProductCreatePydantic(BaseModel):
    name: str
    category_id: uuid.UUID
    image_url: HttpUrl


class ProductCreatedPydantic(BaseModel):
    id: uuid.UUID


@router.post("/")
async def create_product(
    product: ProductCreatePydantic,
    service: ProductsService = Depends(get_products_service),
):
    result = await service.create_product(ProductCreate(**product.dict()))
    return ProductCreatedPydantic(**dataclasses.asdict(result))
