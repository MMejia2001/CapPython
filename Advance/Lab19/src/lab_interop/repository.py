from lab_interop.models import OrderModel


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, OrderModel] = {}

    def save(self, order: OrderModel) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: int) -> OrderModel | None:
        return self._orders.get(order_id)
