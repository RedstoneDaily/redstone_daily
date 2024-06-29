# 将json数据添加到数据库中

import json
from pymongo import MongoClient

# 连接数据库
client = MongoClient()
db = client['redstone_daily']

original = db['original']  # 原始数据
daily = db['daily']        # 今日数据
daily_list = db['daily_list']  # 数据列表

# 读取json文件
with open('data/database_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

