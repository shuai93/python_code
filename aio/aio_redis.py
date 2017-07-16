# import asyncio
# import aioredis
 
# loop = asyncio.get_event_loop()
 
# @asyncio.coroutine
# def go():
#     conn = yield from aioredis.create_connection(
#         ('localhost', 6379), loop=loop)
#     yield from conn.execute('set', 'my-key', 'value')
#     val = yield from conn.execute('get', 'my-key')
#     print(val)
#     conn.close()
# loop.run_until_complete(go())
# will print 'value'


import asyncio
import aioredis
 
loop = asyncio.get_event_loop()
 
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
 
loop.run_until_complete(go())