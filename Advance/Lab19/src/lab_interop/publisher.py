import json
from collections.abc import Callable
from contextlib import suppress

from lab_interop.models import OrderModel


class EventPublisher:
    def __init__(self, publish_func: Callable[[str], None] | None = None) -> None:
        self._publish_func = publish_func
        self.published_messages: list[str] = []

    def publish_order_created(self, order: OrderModel) -> str:
        payload = json.dumps(
            {
                "event": "OrderCreated",
                "order_id": order.order_id,
                "customer": order.customer,
                "total": order.total,
                "status": order.status,
            }
        )
        self.published_messages.append(payload)
        if self._publish_func is not None:
            with suppress(Exception):
                self._publish_func(payload)
        return payload


def redis_publish_factory(channel_name: str = "orders.events"):
    try:
        import redis

        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        return lambda payload: client.publish(channel_name, payload)
    except Exception:
        return None
