import json

import pymongo
from engine.config import config
from cachetools import cached
from cachetools import LRUCache


class Database:
    def __init__(self, host: str, db_name: str):
        self.database = pymongo.MongoClient(host)[db_name]
        self.collection = None

    def set_collection(self, collection_name: str) -> 'Database':
        """
        初始化数据库对象的集合
        :param collection_name:
        :return: Database对象(设置了集合)
        """
        self.collection = self.database[collection_name]

        return self

    @cached(LRUCache(maxsize=128))
    def cache_find_one(self, arg_json_str: str):
        """
        带有LRU缓存的find_one方法
        :param arg_json_str: find_one方法的参数(json字符串)
        :return: 查询结果
        """

        return self.collection.find_one(json.loads(arg_json_str))

    def __getattr__(self, name):
        """
        实现getattr方法，使得可以通过database示例.方法名 调用数据库集合的方法
        :param name: 方法名
        :return: 数据库集合的方法
        """
        if self.collection is None:
            raise ValueError('错误：请先初始化数据库集合')

        return getattr(self.collection, name)


def get_database(collection_name: str = 'redstone_daily', db_name: str ='redstone_daily'):
    """
    获取数据库对象
    :param db_name: 数据库名称
    :param collection_name: 集合名称
    :return: 数据库对象
    """

    database = Database(config.db_host, db_name)
    return database.set_collection(collection_name)


if __name__ == '__main__':
    db = get_database()
