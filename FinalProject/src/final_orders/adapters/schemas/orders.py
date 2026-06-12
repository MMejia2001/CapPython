from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class OrderCreateIn(BaseModel):
    order_id: PositiveInt
    customer: str = Field(min_length=1)
    items: list[OrderItemIn] = Field(min_length=1)


class OrderItemOut(BaseModel):
    sku: str
    name: str
    unit_price: float
    qty: int
    line_total: float


class OrderOut(BaseModel):
    order_id: int
    customer: str
    status: str
    total: float
    items: list[OrderItemOut]
