import grpc

from lab_interop.generated import orders_pb2, orders_pb2_grpc


def main() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = orders_pb2_grpc.OrdersServiceStub(channel)

        response = stub.CreateOrder(
            orders_pb2.CreateOrderRequest(
                order_id=1,
                customer="Marco",
                items=[
                    orders_pb2.OrderItem(sku="A1", unit_price=100.0, qty=2),
                    orders_pb2.OrderItem(sku="B2", unit_price=50.0, qty=1),
                ],
            )
        )
        print("CreateOrder ->", response)

        order = stub.GetOrder(orders_pb2.GetOrderRequest(order_id=1))
        print("GetOrder ->", order)


if __name__ == "__main__":
    main()
