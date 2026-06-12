from fastapi import FastAPI

from final_orders.adapters.api.routes import router as orders_router
from final_orders.config.settings import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(orders_router)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}
