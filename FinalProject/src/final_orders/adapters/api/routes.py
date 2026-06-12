from fastapi import APIRouter, Depends, HTTPException, status

from final_orders.adapters.api.dependencies import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
    require_api_key,
)
from final_orders.adapters.schemas.orders import OrderCreateIn, OrderOut
from final_orders.application.use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
)
from final_orders.domain.entities import Order

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_api_key)])


def to_response(order: Order) -> OrderOut:
    return OrderOut(
        order_id=order.order_id,
        customer=order.customer,
        status=order.status,
        total=order.total,
        items=[
            {
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "qty": item.qty,
                "line_total": item.line_total,
            }
            for item in order.items
        ],
    )


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreateIn,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    order = use_case.execute(
        order_id=payload.order_id,
        customer=payload.customer,
        items=[item.model_dump() for item in payload.items],
    )
    return to_response(order)


@router.get("", response_model=list[OrderOut])
def list_orders(use_case: ListOrdersUseCase = Depends(get_list_orders_use_case)):
    return [to_response(order) for order in use_case.execute()]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    use_case: GetOrderUseCase = Depends(get_get_order_use_case),
):
    order = use_case.execute(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order no encontrada")
    return to_response(order)
