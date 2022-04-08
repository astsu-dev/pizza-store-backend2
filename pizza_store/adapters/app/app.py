from fastapi import FastAPI

from pizza_store.adapters.app.routes.root import router
from pizza_store.adapters.db.client import client


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    @app.on_event("shutdown")
    async def _() -> None:
        await client.aclose()

    return app
