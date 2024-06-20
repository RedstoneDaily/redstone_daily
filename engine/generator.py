import os
import random
import crawler
import json
import time
from datetime import datetime

from bilibili_api import sync, video as bilivideo
from tqdm import tqdm
from pymongo import MongoClient

# 连接数据库
client = MongoClient()
db = client['redstone_daily']

original = db['original']  # 原始数据
daily = db['daily']        # 今日数据

def data_filter(str):
    """
    过滤数据 防止注入
    :param str: 待过滤的字符串
    :return: 过滤后的字符串
    """

    return str.replace("'", '').replace('"', '').replace('$', '').replace('{', '').replace('}', '').replace('regex', '')

def filter_video(title, description, tags, weight_map):
    """
    根据权重列表过滤视频数据
    :param title:
    :param description:
    :param tags:
    :param weight_map:
    :return:
    """
    # 处理标题数据
    flag = False
    tmp_string = ''
    for i in title:
        if i == '<':
            flag = True
        if flag:
            if i == '>':
                flag = False
            continue
        tmp_string += i
    title = tmp_string

    # 创建一个权重,用于分析视频数据
    weight = 0.99

    # 处理全局权重
    for i in weight_map['weight_map']['global']:
        if i['keyword'] in title:
            weight *= i['weight']
        if i['keyword'] in description:
            weight *= i['weight']
        if i['keyword'] in tags:
            weight *= i['weight']

    # 处理关键词
    for i in weight_map['terms']:  # 术语(权重1.5)
        if i in title or i in description or i in tags:
            weight *= 1.5

    for i in weight_map['blacklist']:  # 黑名单(权重0)
        if i in title or i in description or i in tags:
            weight *= 0

    # 处理特殊权重
    for i in weight_map['weight_map']['special']:
        if i['keyword'] in title:
            weight *= i['title'][0]
        if i['keyword'] in description:
            weight *= i['description'][0]
        if i['keyword'] in tags:
            weight *= i['tags'][0]
        if i['keyword'] not in title:
            weight *= i['title'][1]
        if i['keyword'] not in description:
            weight *= i['description'][1]
        if i['keyword'] not in tags:
            weight *= i['tags'][1]

    return weight


# 计算视频综合得分
def calc_score(like, view, favorite, coin, share, review):
    if view == 0:
        return 0
    return (like + share + review) / view * (100 * coin + 25 * favorite) / view


def get_today_video(config, weight_map):
    # 初始化计数器
    i = 0
    print('程序已启动,开始搜索视频')
    time_1 = time.time()

    # 使用crawler模块搜索并获取今日视频列表
    video_list = crawler.search_video(config['search']['keyword'])

    time_2 = time.time()
    print('搜索已完成,共搜索到', len(video_list), '个视频,耗时', time_2 - time_1, '秒,开始筛选视频')

    # 检查视频列表是否为空，如果为空则输出提示信息，并返回'NO_VIDEO'
    if len(video_list) == 0:
        print('今天居然没有视频 ERR_CODE=NO_VIDEO')
        return 'NO_VIDEO'

    # 检查是否需要筛选视频, 如果需要筛选则进行筛选
    if config['search']['enable_screening']:
        # 创建临时变量存储符合规则的视频列表
        temp_video_list = []
        # 遍历所有视频，过滤出符合规则的视频并添加到临时列表中
        for video in tqdm(video_list):
            i += 1
            weight = filter_video(video['title'], video['description'], video['tag'], weight_map)
            temp_video_list.append([video, weight])

        video_list = temp_video_list
        # 将符合规则的视频列表赋值给原视频列表

        time_3 = time.time()
        print('筛选已完成,共筛选到', len(video_list), '个视频,耗时', time_3 - time_2, '秒,开始处理视频')

        # 检查经过筛选后的视频列表是否为空，如果为空则输出提示信息，并返回'NOT_FOUND'
        if len(video_list) == 0:
            print('今天居然没有符合规则的视频 ERR_CODE=NOT_FOUND')
            return 'NOT_FOUND'
    else:
        time_3 = time.time()

    # 初始化结果列表用于存放处理后的视频信息
    result_list = []

    counter = 0
    # 遍历符合规则的视频列表，获取每个视频的各项详细信息
    for video in tqdm(video_list):
        # 解决一下当关闭筛选时视频列表没有权重的问题
        counter += 1
        if not config['search']['enable_screening']:
            video = [video, counter]
        # 创建bilivideo.Video对象并获取其详细信息
        video_obj = bilivideo.Video(bvid=video[0]["bvid"])
        res = sync(video_obj.get_info())

        # 处理标题数据
        new_title = ''
        flag = False
        for i in video[0]['title']:
            if flag or i == '<':
                flag = True
                if i == '>':
                    flag = False
                continue
            new_title += i

        title = new_title  # 视频标题
        description = video[0]['description'].replace('\n', ' ')  # 视频描述
        author = video[0]['author']  # 视频作者
        url = video[0]['arcurl']  # 视频链接
        cover_url = video[0]['pic']  # 视频封面链接
        upic = video[0]['upic']  # UP主头像链接
        play = video[0]['play']  # 视频播放次数
        review = video[0]['review']  # 视频评论数量
        like = video[0]['like']  # 视频点赞数
        coin = res['stat']['coin']  # 视频投币数
        share = res['stat']['share']  # 视频分享数
        favorite = video[0]['favorites']  # 视频收藏数
        pubdate = res['pubdate']  # 视频发布时间
        danmaku = res['stat']['danmaku']  # 视频弹幕数
        score = calc_score(like, play, favorite, coin, share, review)  # 视频综合得分
        weight = video[1]

        result_list.append({
            'title': title,
            'description': description,
            'author': author,
            'url': url,
            'cover_url': cover_url,
            'upic': upic,
            'play': play,
            'review': review,
            'like': like,
            'coin': coin,
            'share': share,
            'favorite': favorite,
            'pubdate': pubdate,
            'danmaku': danmaku,
            'score': score,
            'weight': weight
        })  # 将视频信息添加到结果列表中

        # 为了避免频繁请求，暂停0.5~2秒后再处理下一个视频
        time.sleep(random.uniform(0.5, 2))
    # 返回处理完成的视频信息列表
    time_4 = time.time()
    print('处理已完成耗时', time_4 - time_3, '秒,开始排序')
    return result_list


def transform_video_item(video_item: dict) -> dict:
    return {
        "type": "video",
        "title": data_filter(video_item['title']),  # 使用过滤函数过滤数据
        "description": data_filter(video_item['description']),
        "url": video_item['url'],
        "cover_url": video_item['cover_url'],
        "pubdate": video_item['pubdate'],
        "data": {
            "play": video_item['play'],
            "review": video_item['review'],
            "like": video_item['like'],
            "coin": video_item['coin'],
            "share": video_item['share'],
            "favorite": video_item['favorite'],
            "danmaku": video_item['danmaku'],
            "score": video_item['score']
        },
        "author": {
            "name": data_filter(video_item['author']),
            "upic": video_item['upic']
        }
    }


# 将视频信息写入文件
def write_video_info(video_info_list: list[dict]):
    time_1 = time.time()
    filtered_video_info_list = list(filter(lambda i: i['weight'] > 1, video_info_list))
    # 创建文件字典
    all = {
        "title": time.strftime("%Y-%m-%d", time.localtime()),
        "config": {
            "generate_time": str(datetime.now()),
            "original_video_count": len(video_info_list),
            "filtered_video_count": len(filtered_video_info_list)
        },
        "description": "阿巴阿巴",
        "content": list(map(transform_video_item, video_info_list))
    }
    filtered = all.copy()
    filtered["content"] = list(map(transform_video_item, filtered_video_info_list))

    # 写入数据库
    original.insert_one(all)  # 写入原始数据
    daily.insert_one(filtered)  # 写入今日数据

    time_2 = time.time()
    print('写入数据库已完成,耗时', time_2 - time_1, '秒')


#     update_database_list()

# if __name__ == '__main__':