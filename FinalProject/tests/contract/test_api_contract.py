from fastapi.testclient import TestClient

from final_orders.app import app

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
