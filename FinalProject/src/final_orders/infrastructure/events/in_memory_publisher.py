from final_orders.application.ports import EventPublisher


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.events: list[object] = []

    def publish(self, event: object) -> None:
        self.events.append(event)
