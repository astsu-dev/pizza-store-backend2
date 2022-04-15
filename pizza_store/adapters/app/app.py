from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pizza_store.adapters.app.routes.root import router
from pizza_store.adapters.db.client import client


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("shutdown")
    async def _() -> None:
        await client.aclose()

    return app
