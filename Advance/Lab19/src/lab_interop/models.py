from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OrderItemModel(BaseModel):
    sku: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class OrderModel(BaseModel):
    order_id: PositiveInt
    customer: str = Field(min_length=1)
    items: list[OrderItemModel] = Field(min_length=1)
    status: str = "CREATED"

    @property
    def total(self) -> float:
        return round(sum(item.unit_price * item.qty for item in self.items), 2)
