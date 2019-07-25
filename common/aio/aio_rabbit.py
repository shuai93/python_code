#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

"""
python aio rabbitmq　product
reference https://aio-pika.readthedocs.io/en/latest/
"""

import asyncio
import uuid
import json
import time
from pprint import pprint
from aio_pika import connect, IncomingMessage, Message


def time_wrapper(func, aio=False):
    """
    wrapper函数，用于查看时间
    """
    if aio:
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            await func(*args, **kwargs)
            print("当前代码耗时: {}".format((time.time() - start_time)))
    else:
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            print("当前代码耗时: {}".format((time.time() - start_time)))
    return wrapper


class AioRpcClient:
    def __init__(self, loop, rabbit_mq, queue_name):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop
        self.rabbit_mq = rabbit_mq
        self.queue_name = queue_name

    def build_url(self):
        url = 'amqp://{}:{}@{}:{}/{}'.format(
            self.rabbit_mq['username'],
            self.rabbit_mq['password'],
            self.rabbit_mq['host'],
            self.rabbit_mq['port'],
            self.rabbit_mq['virtual_host']
        )
        return url

    async def connect(self):
        self.connection = await connect(self.build_url(), loop=self.loop)
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(name=self.queue_name)
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        # aio-pika == 0.10.7 不需要 await
        await self.callback_queue.consume(self.on_response)

        return self

    def on_response(self, message: IncomingMessage):
        correlation_id = message.correlation_id
        if correlation_id:
            future = self.futures.pop(message.correlation_id)
            future.set_result(message.body)

    async def call(self, msg, queue_name, rpc=False):
        if rpc:
            correlation_id = str(uuid.uuid4()).encode()
            future = self.loop.create_future()

            self.futures[correlation_id] = future

            await self.channel.default_exchange.publish(
                Message(
                    bytes(json.dumps(msg), 'utf-8'),
                    content_type='text/plain',
                    correlation_id=correlation_id,
                    reply_to=self.callback_queue.name,
                ),
                routing_key=queue_name,
            )

            return await future
        else:
            await self.channel.default_exchange.publish(
                Message(
                    bytes(json.dumps(msg), 'utf-8'),
                    content_type='text/plain',
                ),
                routing_key=queue_name,
            )

async def aio_rpc_client(loop, rabbit_mq, msg, queue_name):
    fibonacci_rpc = await AioRpcClient(loop, rabbit_mq, queue_name).connect()
    print("rabbit 连接建立成功")

    response = await fibonacci_rpc.call(msg, queue_name, rpc=True)
    pprint(json.loads(response))

async def aio_client(loop, rabbit_mq, msg, queue_name):
    fibonacci_rpc = await AioRpcClient(loop, rabbit_mq, queue_name).connect()
    print("rabbit 连接建立成功")

    await fibonacci_rpc.call(msg, queue_name)


@time_wrapper
def rpc_main():
    rabbit_mq = {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'virtual_host': '/'
    }
    msg = {
        "account_mobile": "110",
    }
    queue_name = 'hello'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aio_rpc_client(loop, rabbit_mq, msg, queue_name))
    loop.close()


@time_wrapper
def main():
    rabbit_mq = {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'virtual_host': '/'
    }
    msg = {
        "account_mobile": "110",
    }
    queue_name = 'hello'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aio_client(loop, rabbit_mq, msg, queue_name))
    loop.close()


if __name__ == "__main__":
    main()

