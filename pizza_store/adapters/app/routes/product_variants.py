import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from pizza_store.adapters.app.dependencies import get_current_user, get_products_service
from pizza_store.adapters.app.routes.categories import CategoryPydantic
from pizza_store.services.auth.models import UserTokenData
from pizza_store.services.products.exceptions import (
    ProductNotFoundError,
    ProductVariantNotFoundError,
)
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


class ProductWithoutVariantsPydantic(BaseModel):
    id: uuid.UUID
    name: str
    category: CategoryPydantic
    image_url: str


class ProductVariantWithProductPydantic(BaseModel):
    id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal
    product: ProductWithoutVariantsPydantic


@router.post("")
async def create_product_variant(
    product_id: uuid.UUID,
    product_variant: ProductVariantCreatePydantic,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductVariantCreatedPydantic:
    try:
        result = await service.create_product_variant(
            ProductVariantCreate(
                product_id=product_id,
                name=product_variant.name,
                weight=product_variant.weight,
                weight_units=product_variant.weight_units,
                price=product_variant.price,
            )
        )
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist."
        )
    return ProductVariantCreatedPydantic(id=result.id)


@router.delete("/{id}")
async def delete_product_variant(
    id: uuid.UUID,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductVariantDeletedPydantic:
    try:
        result = await service.delete_product_variant(id)
    except ProductVariantNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant does not exist.",
        )
    return ProductVariantDeletedPydantic(id=result.id)


@router.put("/{id}")
async def update_product_variant(
    id: uuid.UUID,
    product_variant: ProductVariantUpdatePydantic,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductVariantUpdatedPydantic:
    try:
        result = await service.update_product_variant(
            ProductVariantUpdate(
                id=id,
                name=product_variant.name,
                weight=product_variant.weight,
                weight_units=product_variant.weight_units,
                price=product_variant.price,
            )
        )
    except ProductVariantNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant does not exist.",
        )
    return ProductVariantUpdatedPydantic(id=result.id)
