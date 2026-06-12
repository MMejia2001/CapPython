from lab_interop.models import OrderItemModel, OrderModel
from lab_interop.publisher import EventPublisher


def test_publish_order_created_returns_json_message():
    publisher = EventPublisher()
    order = OrderModel(
        order_id=1,
        customer="Marco",
        items=[OrderItemModel(sku="A1", unit_price=25.0, qty=2)],
    )

    payload = publisher.publish_order_created(order)

    assert "OrderCreated" in payload
    assert '"order_id": 1' in payload
