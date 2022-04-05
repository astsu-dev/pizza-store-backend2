import uvicorn
from fastapi import FastAPI

from pizza_store.adapters.app.routes.root import router
from pizza_store.adapters.db.client import client

app = FastAPI()
app.include_router(router)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await client.aclose()


if __name__ == "__main__":
    uvicorn.run(
        "pizza_store.adapters.app.app:app", host="127.0.0.1", port=8000, reload=True
    )
