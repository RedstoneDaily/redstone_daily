import json

from engine.utils.data.database import get_database

api_response_string = input()

data = json.loads(api_response_string)

formatted_data = []
# 剔除无用数据

for i in data:

    # 如果i['content']为图片链接, 则标记为图片
    if i['content'].startswith('http') and \
            (i['content'].endswith('.jpg') or i['content'].endswith('.png')):

        formatted_data.append({"type": "image", "content": i['content']})

    # 如果i['content']为卡片内容, 则标记为卡片
    elif i['content'].startswith('[{\"type\":\"card\"'):

        card = json.loads(i['content'])

        if card[0]['modules'][0]['canDownload']:
            formatted_data.append({"type": "card", "content": card[0]['modules'][0]['src']})

    # 剩下的内容均为文字
    elif not i['content'].startswith('[{"'):

        # 剔除归档日志
        if i['author']['nickname'] == '技术管理shinya':
            continue

        formatted_data.append({"type": "text", "content": i['content']})

result = []

# 整理数据结构
# 对每两个`card`之间的数据进行分组

last_card = 0
for i in range(len(formatted_data)):
    if formatted_data[i]['type'] == 'card':
        tmp = {"content": '', "imgs": [], "url": ''}
        while last_card <= i:
            if formatted_data[last_card]['type'] == 'card':
                tmp['url'] = formatted_data[last_card]['content']
            elif formatted_data[last_card]['type'] == 'image':
                tmp['imgs'].append(formatted_data[last_card]['content'])
            else:
                tmp['content'] += (formatted_data[last_card]['content'] + '\n')

            last_card += 1
        result.append(tmp)

# 输出结果
print(json.dumps(result, ensure_ascii=False))

index_db = get_database('config', 'rd_archives')
index = index_db.find_one({'tag': 'config'})['max_id']

# 添加id
for i in range(len(result)):
    result[i]['id'] = index
    index += 1

get_database('wreg', 'rd_archives').insert_many(result)

index_db.update_one({'tag': 'config'}, {'$set': {'max_id': index}})
