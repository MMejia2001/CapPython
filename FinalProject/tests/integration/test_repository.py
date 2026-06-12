from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from final_orders.domain.entities import Order, OrderItem
from final_orders.infrastructure.db.base import Base
from final_orders.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


def test_repository_saves_order_in_sqlite_memory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repo = SqlAlchemyOrderRepository(session)
        order = Order(
            order_id=1,
            customer="Marco",
            items=[OrderItem(sku="A1", name="Mouse", unit_price=100.0, qty=1)],
        )
        repo.add(order)

        loaded = repo.get(1)

    assert loaded is not None
    assert loaded.customer == "Marco"
    assert loaded.total == 100.0
