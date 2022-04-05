from fastapi import APIRouter

from pizza_store.adapters.app.routes.categories import router as categories_router
from pizza_store.adapters.app.routes.products import router as products_router

router = APIRouter()
router.include_router(categories_router)
router.include_router(products_router)
