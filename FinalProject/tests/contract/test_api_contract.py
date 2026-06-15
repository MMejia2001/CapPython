from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from final_orders.adapters.api.dependencies import get_session
from final_orders.app import app
from final_orders.infrastructure.db.base import Base

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def override_get_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)
HEADERS = {"x-api-key": "demo-key"}


def test_create_order_contract():
    response = client.post(
        "/orders",
        headers=HEADERS,
        json={
            "order_id": 1,
            "customer": "Marco",
            "items": [{"sku": "A1", "name": "Mouse", "unit_price": 100, "qty": 1}],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["order_id"] == 1
    assert body["status"] == "CREATED"
    assert body["total"] == 100.0
