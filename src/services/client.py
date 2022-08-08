import sys
import asyncio
import logging
import random

import grpc
from src.services.proto import service_pb2_grpc
from src.services.proto.service_pb2 import HelloRequest, HelloReply
import json, time
from config import CONFIG


logger = logging.getLogger(__name__)
_NAMES = ['Cole', 'Raychel', 'Bumpkin', 'Dingle', 'Butchnugget', 'Darling']


async def run() -> None:
    try:
        async with grpc.aio.insecure_channel(f'invoke-receiver:{CONFIG.SERVER_GRPC_PORT}') as channel:
            while True:
                metadata = (('dapr-app-id', 'invoke-receiver'),)
                stub = service_pb2_grpc.HelloWorldServiceStub(channel)
                response: HelloReply = await stub.SayHello(request=HelloRequest(name=random.choice(_NAMES)), metadata=metadata)
                logger.info("Greeter client received: " + response.message)
                await asyncio.sleep(5)
    except Exception as ex:
        logger.info(f"Oh crap")
        raise ex

if __name__ == '__main__':
    logger.info('I am in main')
    logging.basicConfig()
    asyncio.run(run())
