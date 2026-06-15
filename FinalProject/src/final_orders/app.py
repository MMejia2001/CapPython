from contextlib import asynccontextmanager

from fastapi import FastAPI

from final_orders.adapters.api.routes import router as orders_router
from final_orders.config.settings import settings
from final_orders.infrastructure.db.base import Base
from final_orders.infrastructure.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(orders_router)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}
