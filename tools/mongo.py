# -*- coding: utf-8 -*-

import urllib.parse
import asyncio
import motor
from motor.motor_asyncio import AsyncIOMotorClient
# from cachetools import cached, LRUCache, TTLCache

from config.settings import settings


class Mongo(object):
    def __init__(self):
        self.host = settings.get('MONGO_HOST')
        self.port = settings.get('MONGO_PORT')
        self.user = settings.get('MONGO_USER')
        self.password = settings.get('MONGO_PASS')

    async def return_result(self, result):
        return result

    async def client(self):
        username = urllib.parse.quote_plus(self.user)
        password = urllib.parse.quote_plus(self.password)
        mongodb_uri = 'mongodb://%s:%s@%s:%s' % (username, password, self.host, self.port)
        client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
        return client

    async def db(self, database='workflow'):
        if not database:
            database = settings.get('MONGO_DB')
        client = await self.client()
        db = client[database]
        return db

#     async def database(self, database):
#         client = await self.client()
#         database = client[database]
#         return database
#
#     async def collection(self, database, collection):
#         database = await self.database(database)
#         collection = database[collection]
#         return collection
#
#     async def create_index(self, database, collection, keys, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.create_index(keys, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def create_indexes(self, database, collection, keys, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.create_indexes(keys, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def drop_index(self, database, collection, index, session=None, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.drop_index(index, session, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def drop_indexes(self, database, collection, session=None, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.drop_indexes(session, **kwargs)
#         print('result %s' % result)
#         return result
#
#     # @cached(cache=LRUCache(maxsize=2048))
#     async def find_one(self, database, collection, query, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.find_one(query, kwargs)
#         print('result_one %s' % result)
#         return result
#
#     # @cached(cache=LRUCache(maxsize=2048))
#     async def find_many(self, database, collection, query, **kwargs):
#         collection = await self.collection(database, collection)
#         result = collection.find(query, kwargs)
#         print('result_many %s' % result)
#         return result
#
#     async def update_one(self, database, collection, query, document, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.update_one(query, document, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def update_many(self, database, collection, query, document, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.update_many(query, document, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def insert_one(self, database, collection, document, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.insert_one(document, **kwargs)
#         print('result %s' % repr(result.inserted_id))
#         return result
#
#     async def insert_many(self, database, collection, document, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.insert_many(document, **kwargs)
#         print('result %s' % repr(result))
#         return result
#
#     async def delete_one(self, database, collection, query, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.delete_one(query, **kwargs)
#         print('result %s' % result)
#         return result
#
#     async def delete_many(self, database, collection, query, **kwargs):
#         collection = await self.collection(database, collection)
#         result = await collection.delete_many(query, **kwargs)
#         print('result %s' % result)
#         return result
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(Mongo().insert_one('database_1', 'collection_1', {'key1': 'val1', 'key2': 100}))
#     loop.run_until_complete(Mongo().find_many('database_1', 'collection_1', { 'key1': "val1"}, **{"0": 0}))
#     loop.run_until_complete(Mongo().find_many('database_1', 'collection_1', { 'key1': { '$regex': 'val', '$options': 'i' } }, **{"key1": 1, "key2": 1}))
#     loop.run_until_complete(Mongo().create_index('database_1', 'collection_1', [('key1', "text")]))
#     loop.run_until_complete(Mongo().delete_many('database_1', 'collection_1', {'key1': 'val1'}))


