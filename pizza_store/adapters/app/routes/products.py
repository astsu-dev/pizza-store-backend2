import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.networks import HttpUrl

from pizza_store.adapters.app.dependencies import get_current_user, get_products_service
from pizza_store.adapters.app.routes.categories import CategoryPydantic
from pizza_store.adapters.app.routes.product_variants import ProductVariantPydantic
from pizza_store.services.auth.models import UserTokenData
from pizza_store.services.products.models import ProductCreate, ProductUpdate
from pizza_store.services.products.service import ProductsService

router = APIRouter(prefix="/products")


class ProductCreatePydantic(BaseModel):
    name: str
    category_id: uuid.UUID
    image_url: HttpUrl


class ProductCreatedPydantic(BaseModel):
    id: uuid.UUID


class ProductDeletedPydantic(BaseModel):
    id: uuid.UUID


ProductUpdatePydantic = ProductCreatePydantic


class ProductUpdatedPydantic(BaseModel):
    id: uuid.UUID


class ProductPydantic(BaseModel):
    id: uuid.UUID
    name: str
    category: CategoryPydantic
    variants: list[ProductVariantPydantic]
    image_url: str


@router.post("")
async def create_product(
    product: ProductCreatePydantic,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductCreatedPydantic:
    result = await service.create_product(
        ProductCreate(
            name=product.name,
            category_id=product.category_id,
            image_url=product.image_url,
        )
    )
    return ProductCreatedPydantic(id=result.id)


@router.get("")
async def get_products(
    category_id: uuid.UUID | None = None,
    service: ProductsService = Depends(get_products_service),
) -> list[ProductPydantic]:
    result = await service.get_products(category_id=category_id)
    return [
        ProductPydantic(
            id=p.id,
            name=p.name,
            category=CategoryPydantic(id=p.category.id, name=p.category.name),
            variants=[
                ProductVariantPydantic(
                    id=v.id,
                    name=v.name,
                    weight=v.weight,
                    weight_units=v.weight_units,
                    price=v.price,
                )
                for v in p.variants
            ],
            image_url=p.image_url,
        )
        for p in result
    ]


@router.get("/{id}")
async def get_product(
    id: uuid.UUID,
    service: ProductsService = Depends(get_products_service),
) -> ProductPydantic:
    result = await service.get_product(id)
    return ProductPydantic(
        id=result.id,
        name=result.name,
        category=CategoryPydantic(id=result.category.id, name=result.category.name),
        variants=[
            ProductVariantPydantic(
                id=v.id,
                name=v.name,
                weight=v.weight,
                weight_units=v.weight_units,
                price=v.price,
            )
            for v in result.variants
        ],
        image_url=result.image_url,
    )


@router.delete("/{id}")
async def delete_product(
    id: uuid.UUID,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductDeletedPydantic:
    result = await service.delete_product(id)
    return ProductDeletedPydantic(id=result.id)


@router.put("/{id}")
async def update_product(
    id: uuid.UUID,
    product: ProductUpdatePydantic,
    service: ProductsService = Depends(get_products_service),
    _: UserTokenData = Depends(get_current_user(is_admin_required=True)),
) -> ProductUpdatedPydantic:
    result = await service.update_product(
        ProductUpdate(
            id=id,
            name=product.name,
            category_id=product.category_id,
            image_url=product.image_url,
        )
    )
    return ProductUpdatedPydantic(id=result.id)
