from lab_interop.generated import orders_pb2
from lab_interop.publisher import EventPublisher
from lab_interop.repository import InMemoryOrderRepository
from lab_interop.service import OrdersApplicationService


def test_create_order_saves_and_publishes_event():
    publisher = EventPublisher()
    service = OrdersApplicationService(InMemoryOrderRepository(), publisher)

    response = service.create_order(
        orders_pb2.CreateOrderRequest(
            order_id=1,
            customer="Marco",
            items=[orders_pb2.OrderItem(sku="A1", unit_price=100.0, qty=2)],
        )
    )

    assert response.order.order_id == 1
    assert response.order.total == 200.0
    assert len(publisher.published_messages) == 1
    assert "OrderCreated" in publisher.published_messages[0]
