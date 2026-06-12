from final_orders.domain.entities import Order, OrderItem


def test_order_total_is_calculated():
    order = Order(
        order_id=1,
        customer="Marco",
        items=[
            OrderItem(sku="A1", name="Mouse", unit_price=100.0, qty=2),
            OrderItem(sku="B2", name="Keyboard", unit_price=50.0, qty=1),
        ],
    )

    assert order.total == 250.0


def test_order_requires_items():
    order = Order(order_id=1, customer="Marco", items=[])

    try:
        order.validate()
    except ValueError as exc:
        assert "al menos 1 item" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError")
