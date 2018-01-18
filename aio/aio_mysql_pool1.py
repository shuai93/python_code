#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

import asyncio
from aiomysql import create_pool

"""
aio_mysql_pool 
创建 M_POOL 连接池对象

reference https://aiomysql.readthedocs.io/en/latest/
github https://github.com/aio-libs/aiomysql

"""


M_POOL = None


async def get_mysql_connect(mysql_dict=None, loop=None):
    global M_POOL
    if M_POOL:
        return M_POOL
    # minsize　最小连接数 默认是1, maxsize 最大连接数 默认是10
    M_POOL = await create_pool(minsize=2, maxsize=8, **mysql_dict, loop=loop)
    return M_POOL


async def query(loop, mysql):
    pool = await get_mysql_connect(mysql_dict=mysql, loop=loop)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id_no,clt_nm FROM t_client;")
            print(cur.description)
            # 这里的操作类似 pymysql

            # (r, s) = await cur.fetchone()
            # print(r, s)
            result = await cur.fetchall()
            print(len(result))
            # then you can do something


def start():
    mysql_params = {
        "host": '127.0.0.1',
        "port": 3306,
        "user": 'root',
        "password": 'root',
        "db": 'base_info',
        "charset": 'utf8'
    }
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query(loop, mysql_params))
    # loop.close()

if __name__ == "__main__":
    start()
