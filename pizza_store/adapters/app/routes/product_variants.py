import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pizza_store.adapters.app.dependencies import get_products_service
from pizza_store.services.products.models import (
    ProductVariantCreate,
    ProductVariantUpdate,
)
from pizza_store.services.products.service import ProductsService

router = APIRouter(prefix="/product-variants")


class ProductVariantCreatePydantic(BaseModel):
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


class ProductVariantCreatedPydantic(BaseModel):
    id: uuid.UUID


class ProductVariantDeletedPydantic(BaseModel):
    id: uuid.UUID


ProductVariantUpdatePydantic = ProductVariantCreatePydantic


class ProductVariantUpdatedPydantic(BaseModel):
    id: uuid.UUID


class ProductVariantPydantic(BaseModel):
    id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


@router.post("")
async def create_product_variant(
    product_id: uuid.UUID,
    product_variant: ProductVariantCreatePydantic,
    service: ProductsService = Depends(get_products_service),
) -> ProductVariantCreatedPydantic:
    result = await service.create_product_variant(
        ProductVariantCreate(
            product_id=product_id,
            name=product_variant.name,
            weight=product_variant.weight,
            weight_units=product_variant.weight_units,
            price=product_variant.price,
        )
    )
    return ProductVariantCreatedPydantic(id=result.id)


@router.delete("/{id}")
async def delete_product_variant(
    id: uuid.UUID,
    service: ProductsService = Depends(get_products_service),
) -> ProductVariantDeletedPydantic:
    result = await service.delete_product_variant(id)
    return ProductVariantDeletedPydantic(id=result.id)


@router.put("/{id}")
async def update_product_variant(
    id: uuid.UUID,
    product_variant: ProductVariantUpdatePydantic,
    service: ProductsService = Depends(get_products_service),
) -> ProductVariantUpdatedPydantic:
    result = await service.update_product_variant(
        ProductVariantUpdate(
            id=id,
            name=product_variant.name,
            weight=product_variant.weight,
            weight_units=product_variant.weight_units,
            price=product_variant.price,
        )
    )
    return ProductVariantUpdatedPydantic(id=result.id)
