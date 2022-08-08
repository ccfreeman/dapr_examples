import logging

import grpc
from src.services.proto import service_pb2_grpc
from src.services.proto.service_pb2 import HelloRequest, HelloReply
from dapr.ext.grpc import App
from config import CONFIG


logger = logging.getLogger(__name__)


class HelloWorldService(service_pb2_grpc.HelloWorldService):

    def SayHello(
        self, request: HelloRequest, context: grpc.aio.ServicerContext
    ) -> HelloReply:
        logger.info(request)
        return HelloReply(message='Hello, %s!' % request.name)

app = App()

if __name__ == '__main__':
    logger.info('starting the HelloWorld Service')
    app.add_external_service(service_pb2_grpc.add_HelloWorldServiceServicer_to_server, HelloWorldService())
    app.run(CONFIG.SERVER_GRPC_PORT)
