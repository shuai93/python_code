#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

import logging
import random
import asyncio
import re
from aiomysql import create_pool


"""
aio_mysql pool 使用方法一
代码未实际运行

reference https://aiomysql.readthedocs.io/en/latest/
github https://github.com/aio-libs/aiomysql

"""

# 假设mysql表分散在8个host, 每个host有16张子表
TABLES = {
    "192.168.1.01": "table_000-015",    # 000-015表示该ip下的表明从table_000一直连续到table_015
    "192.168.1.02": "table_016-031",
    "192.168.1.03": "table_032-047",
    "192.168.1.04": "table_048-063",
    "192.168.1.05": "table_064-079",
    "192.168.1.06": "table_080-095",
    "192.168.1.07": "table_096-0111",
    "192.168.1.08": "table_112-0127",
}
USER = "root"
PASSWD = "root"


def query_wrapper(func):
    """
    wrapper函数，用于捕捉异常
    """
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper


#
@query_wrapper
async def query_do_something(ip, db, table):
    """
    实际的sql访问处理函数，通过aiomysql实现异步非阻塞请求
    :param ip: mysql_host
    :param db: mysql_db
    :param table: mysql_table
    """
    async with create_pool(host=ip, db=db, user=USER, password=PASSWD) as pool:
        async with pool.get() as conn:
            async with conn.cursor() as cur:
                sql = """select * from {} where test"""
                await cur.execute(sql.format(table))
                result = await cur.fetchall()
                # then do something...
                print(result)
                pass


#
def gen_tasks():
    """
    生成sql访问队列, 队列的每个元素包含要对某个表进行访问的函数及参数
    """
    tasks = []
    for ip, table in TABLES.items():
        cols = re.split('_|-', table)
        tblpre = "_".join(cols[:-2])
        min_num = int(cols[-2])
        max_num = int(cols[-1])
        for num in range(min_num, max_num+1):
            tasks.append(
               (query_do_something, ip, 'your_dbname', '{}_{}'.format(tblpre, num))
            )
    # 随机打乱task
    random.shuffle(tasks)
    return tasks


def run_tasks(tasks, batch_len, loop):
    """
    按批量运行sql访问请求队列
    :param tasks: 任务列表
    :param batch_len: 单次执行任务数量
    :param loop: loop
    """
    try:
        for idx in range(0, len(tasks), batch_len):
            batch_tasks = tasks[idx:idx+batch_len]
            logging.info("current batch, start_idx:%s len:%s" % (idx, len(batch_tasks)))
            for i in range(0, len(batch_tasks)):
                l = batch_tasks[i]
                batch_tasks[i] = asyncio.ensure_future(
                    l[0](*l[1:])
                )
            loop.run_until_complete(asyncio.gather(*batch_tasks))
    except Exception as e:
        logging.warn(e)


def main():
    """
    通过asyncio实现函数异步调用
    """
    loop = asyncio.get_event_loop()

    tasks = gen_tasks()
    batch_len = len(TBLES.keys()) * 5   # all up to you like 步长
    run_tasks(tasks, batch_len, loop)

    loop.close()


if __name__ == "__main__":
    main()
