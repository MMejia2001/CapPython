from dataclasses import dataclass


@dataclass(slots=True)
class OrderCreated:
    order_id: int
    customer: str
    total: float
