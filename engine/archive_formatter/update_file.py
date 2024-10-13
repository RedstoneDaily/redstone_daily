import pymongo

from engine.config import config
from engine.utils.data.database import get_database

print('开始更新文件数据...')
target_collection = get_database('archive')

# 获取数据库集合
archive_db = pymongo.MongoClient(config.db_host)['rd_archives']
collections = archive_db.list_collection_names()

print(collections)

# 删除目标数据库中原有数据
target_collection.delete_many({})

# 遍历所有集合，将数据更新到目标数据库
for i in collections:
    if i == 'config':
        continue

    print('正在更新集合：', i)
    collection = archive_db[i]
    for j in collection.find():
        j['source'] = i
        target_collection.update_one({'_id': j['_id']}, {'$set': j}, upsert=True)

print('文件数据更新完成！')