from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from final_orders.adapters.api.dependencies import get_session
from final_orders.app import app
from final_orders.infrastructure.db.base import Base

engine = create_engine("sqlite:///:memory:")
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


def test_full_orders_flow():
    create_response = client.post(
        "/orders",
        headers=HEADERS,
        json={
            "order_id": 10,
            "customer": "Ana",
            "items": [{"sku": "P1", "name": "Pen", "unit_price": 20, "qty": 2}],
        },
    )
    assert create_response.status_code == 201

    list_response = client.get("/orders", headers=HEADERS)
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    get_response = client.get("/orders/10", headers=HEADERS)
    assert get_response.status_code == 200
    assert get_response.json()["customer"] == "Ana"
