from fastapi import APIRouter

from pizza_store.adapters.app.routes.categories import router as category_router

router = APIRouter()
router.include_router(category_router)
