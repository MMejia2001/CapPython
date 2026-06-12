from sqlalchemy.orm import Session, selectinload

from final_orders.application.ports import OrderRepository
from final_orders.domain.entities import Order, OrderItem
from final_orders.infrastructure.db.models import OrderItemModel, OrderModel


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, order: Order) -> None:
        db_order = OrderModel(id=order.order_id, customer=order.customer, status=order.status)
        db_order.items = [
            OrderItemModel(
                sku=item.sku,
                name=item.name,
                unit_price=item.unit_price,
                qty=item.qty,
            )
            for item in order.items
        ]
        self.session.add(db_order)
        self.session.commit()

    def get(self, order_id: int) -> Order | None:
        db_order = (
            self.session.query(OrderModel)
            .options(selectinload(OrderModel.items))
            .filter(OrderModel.id == order_id)
            .first()
        )
        if db_order is None:
            return None
        return self._to_domain(db_order)

    def list_all(self) -> list[Order]:
        rows = self.session.query(OrderModel).options(selectinload(OrderModel.items)).all()
        return [self._to_domain(row) for row in rows]

    def _to_domain(self, db_order: OrderModel) -> Order:
        return Order(
            order_id=db_order.id,
            customer=db_order.customer,
            status=db_order.status,
            items=[
                OrderItem(
                    sku=item.sku,
                    name=item.name,
                    unit_price=item.unit_price,
                    qty=item.qty,
                )
                for item in db_order.items
            ],
        )
