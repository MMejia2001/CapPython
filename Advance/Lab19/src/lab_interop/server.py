from concurrent import futures

import grpc

from lab_interop.generated import orders_pb2, orders_pb2_grpc
from lab_interop.publisher import EventPublisher, redis_publish_factory
from lab_interop.repository import InMemoryOrderRepository
from lab_interop.service import OrdersApplicationService


class OrdersGrpcService(orders_pb2_grpc.OrdersServiceServicer):
    def __init__(self) -> None:
        publisher = EventPublisher(redis_publish_factory())
        self.app_service = OrdersApplicationService(InMemoryOrderRepository(), publisher)

    def CreateOrder(self, request, context):
        return self.app_service.create_order(request)

    def GetOrder(self, request, context):
        order = self.app_service.get_order(request.order_id)
        if order is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.Order()
        return order


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    orders_pb2_grpc.add_OrdersServiceServicer_to_server(OrdersGrpcService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
