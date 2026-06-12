from final_orders.application.ports import EventPublisher, OrderRepository
from final_orders.domain.entities import Order, OrderItem


class CreateOrderUseCase:
    def __init__(self, repository: OrderRepository, publisher: EventPublisher) -> None:
        self.repository = repository
        self.publisher = publisher

    def execute(self, order_id: int, customer: str, items: list[dict]) -> Order:
        order = Order(
            order_id=order_id,
            customer=customer,
            items=[
                OrderItem(
                    sku=str(item["sku"]),
                    name=str(item["name"]),
                    unit_price=float(item["unit_price"]),
                    qty=int(item["qty"]),
                )
                for item in items
            ],
        )
        order.validate()
        order.mark_created()
        self.repository.add(order)
        for event in order.events:
            self.publisher.publish(event)
        return order


class GetOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: int) -> Order | None:
        return self.repository.get(order_id)


class ListOrdersUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Order]:
        return self.repository.list_all()
