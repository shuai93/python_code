#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

"""
aio_redis poll
reference https://aiomysql.readthedocs.io/en/latest/
github https://github.com/aio-libs/aioredis

"""


import asyncio
import aioredis


loop = asyncio.get_event_loop()


# python3.5 之前
@asyncio.coroutine
def go():
    pool = yield from aioredis.create_pool(
        ('localhost', 6379),
        minsize=5, maxsize=10,
        loop=loop)
    with (yield from pool) as redis:    # high-level redis API instance
        yield from redis.set('my-key', 'value')
        print((yield from redis.get('my-key')))
    pool.clear()    # closing all open connections



R_POOL = None

async def get_redis_connect():
    global R_POOL
    if R_POOL:
        return R_POOL
    R_POOL = await aioredis.create_pool('redis://localhost')

    return R_POOL

# python3.5 之后
async def redis_example():
    pool = await get_redis_connect()
    await pool.execute("set", "my-key", "aio-redis")
    val = await pool.execute('get', 'my-key')
    print(val)


def main():
    # loop.run_until_complete(go())
    loop.run_until_complete(redis_example())


if __name__ == "__main__":
    main()
