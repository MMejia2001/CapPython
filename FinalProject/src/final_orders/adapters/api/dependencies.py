from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from final_orders.application.use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
)
from final_orders.config.settings import settings
from final_orders.infrastructure.db.session import get_session
from final_orders.infrastructure.events.in_memory_publisher import InMemoryEventPublisher
from final_orders.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


def require_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(status_code=401, detail="API key inválida")


def get_create_order_use_case(session: Session = Depends(get_session)) -> CreateOrderUseCase:
    repo = SqlAlchemyOrderRepository(session)
    publisher = InMemoryEventPublisher()
    return CreateOrderUseCase(repo, publisher)


def get_get_order_use_case(session: Session = Depends(get_session)) -> GetOrderUseCase:
    return GetOrderUseCase(SqlAlchemyOrderRepository(session))


def get_list_orders_use_case(session: Session = Depends(get_session)) -> ListOrdersUseCase:
    return ListOrdersUseCase(SqlAlchemyOrderRepository(session))
