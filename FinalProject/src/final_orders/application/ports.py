from __future__ import annotations

from abc import ABC, abstractmethod

from final_orders.domain.entities import Order


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None: ...

    @abstractmethod
    def get(self, order_id: int) -> Order | None: ...

    @abstractmethod
    def list_all(self) -> list[Order]: ...


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: object) -> None: ...
