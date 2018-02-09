#!/usr/bin/env python3  
# @Time    : 18-1-22 下午2:15
# @Author  : ys
# @Email   : youngs@yeah.net

"""
aio mongo 

reference http://motor.readthedocs.io/en/stable/tutorial-asyncio.html

查询语法类似 pymongo

# 批量更新
db.User.find().forEach(
   function(item){                
       db.User.update({"_id":item._id},{"$set":{"LastUpdate":item.CreateAt}},false,true)
    }
)
"""

import asyncio
import motor.motor_asyncio

MONGO = {
        "host": "localhost",
        'port': 27017,
        "user": "root",
        "password": "root",
        "authSource": "admin",
        'db': 'test',
        "uri": "mongodb://{user}:{password}@{host}:{port}/{db}?authSource={authSource}"
}


class AioMongo(object):
    """
    aio mongo 
    简单使用
    """

    def __init__(self, parameters=None):
        self.parameters = parameters
        if self.parameters:
            uri = self.parameters['uri'].format(**self.parameters)
            client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self.db = client[self.parameters.get("db", "test")]
        else:
            client = motor.motor_asyncio.AsyncIOMotorClient()
            self.db = client["test"]

    async def do_insert(self, table, query: dict):
        # 单个插入
        result = await self.db[table].insert_one(document=query)
        print('result %s' % repr(result.inserted_id))

    async def do_find_one(self, table, query: dict):
        # 单个查询
        document = await self.db[table].find_one(query)
        print(document)

    async def do_find(self, table, query: dict):
        cursor = self.db[table].find(query)
        # length is necessary
        for document in await cursor.to_list(length=100):
            print(document)

    async def do_find_fancy(self, table, query: dict, limit=0, skip=0):
        # 花式查询
        cursor = self.db[table].find(query)
        # Modify the query before iterating
        cursor.sort('i', -1).limit(limit).skip(skip)
        async for document in cursor:
            print(document)

    async def do_replace(self, table, query: dict, document: dict):
        # 替换
        coll = self.db[table]
        old_document = await coll.find_one(query)
        _id = old_document['_id']
        result = await coll.replace_one({'_id': _id}, document)
        print("result: {}".format(result))
        new_document = await coll.find_one({'_id': _id})
        print(new_document)

    async def do_update(self, table, query: dict, document: dict):
        # 更新
        coll = self.db[table]
        result = await coll.update_one(query, {'$set': document})
        print('updated %s document' % result.modified_count)
        new_document = await coll.find_one(query)
        print(new_document)

    async def do_delete_many(self, table, query: dict):
        # 删除
        coll = self.db[table]
        n = await coll.count()
        print('%s documents before calling delete_many()' % n)
        await self.db[table].delete_many(query)
        print('%s documents after' % (await coll.count()))

    def run(self):
        pass


def main():
    mongo = AioMongo()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mongo.do_delete_many("test", {'i': {'$gte': 50}}))


if __name__ == "__main__":
    main()
