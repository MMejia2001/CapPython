from lab_interop.generated import orders_pb2
from lab_interop.models import OrderItemModel, OrderModel
from lab_interop.publisher import EventPublisher
from lab_interop.repository import InMemoryOrderRepository


class OrdersApplicationService:
    def __init__(
        self,
        repository: InMemoryOrderRepository,
        publisher: EventPublisher,
    ) -> None:
        self.repository = repository
        self.publisher = publisher

    def create_order(self, request: orders_pb2.CreateOrderRequest) -> orders_pb2.CreateOrderResponse:
        order = OrderModel(
            order_id=request.order_id,
            customer=request.customer,
            items=[
                OrderItemModel(sku=item.sku, unit_price=item.unit_price, qty=item.qty)
                for item in request.items
            ],
        )
        self.repository.save(order)
        self.publisher.publish_order_created(order)
        return orders_pb2.CreateOrderResponse(
            message="Order created",
            order=self._to_proto(order),
        )

    def get_order(self, order_id: int) -> orders_pb2.Order | None:
        order = self.repository.get(order_id)
        if order is None:
            return None
        return self._to_proto(order)

    def _to_proto(self, order: OrderModel) -> orders_pb2.Order:
        return orders_pb2.Order(
            order_id=order.order_id,
            customer=order.customer,
            items=[
                orders_pb2.OrderItem(
                    sku=item.sku,
                    unit_price=item.unit_price,
                    qty=item.qty,
                )
                for item in order.items
            ],
            total=order.total,
            status=order.status,
        )
