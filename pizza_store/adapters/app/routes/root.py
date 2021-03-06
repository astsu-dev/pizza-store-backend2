from fastapi import APIRouter

from pizza_store.adapters.app.routes.auth import router as auth_router
from pizza_store.adapters.app.routes.categories import router as categories_router
from pizza_store.adapters.app.routes.orders import router as orders_router
from pizza_store.adapters.app.routes.product_variants import (
    router as product_variants_router,
)
from pizza_store.adapters.app.routes.products import router as products_router

router = APIRouter()
router.include_router(categories_router)
router.include_router(products_router)
router.include_router(product_variants_router)
router.include_router(orders_router)
router.include_router(auth_router)
