from dataclasses import dataclass, field

from final_orders.domain.events import OrderCreated


@dataclass(slots=True)
class OrderItem:
    sku: str
    name: str
    unit_price: float
    qty: int

    @property
    def line_total(self) -> float:
        return round(self.unit_price * self.qty, 2)


@dataclass(slots=True)
class Order:
    order_id: int
    customer: str
    items: list[OrderItem]
    status: str = "CREATED"
    events: list[object] = field(default_factory=list)

    def validate(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id debe ser mayor a 0")
        if not self.customer.strip():
            raise ValueError("customer es requerido")
        if not self.items:
            raise ValueError("la orden debe tener al menos 1 item")

    @property
    def total(self) -> float:
        return round(sum(item.line_total for item in self.items), 2)

    def mark_created(self) -> None:
        self.events.append(OrderCreated(self.order_id, self.customer, self.total))
