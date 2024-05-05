from bilibili_api import search, sync, video, video_zone
import time, sys
from tqdm import tqdm

def search_from_bilibili(page, keyword):
    # 搜索类型，这里指定为视频
    search_type = search.SearchObjectType.VIDEO
    # 排序类型，这里指定为综合排序
    order_type = search.OrderVideo.PUBDATE

    # 同步执行搜索函数
    print(page)
    res = sync(search.search_by_type(keyword, search_type=search_type, order_type=order_type, video_zone_type=video_zone.VideoZoneTypes.GAME, page=page, page_size=20))

    # 过滤出最近1天的视频
    recent_videos = []
    targetTime = time.time() - 86400
    min = 86400
    for i in res['result']:
        interval = i['pubdate'] - targetTime
        if interval > 0:
            recent_videos.append(i)
            if min > interval:
                min = interval
    return recent_videos


def search_video(keyword):
    i = 1
    def search(i):
        result = search_from_bilibili(i, keyword)
        for j in result:
            search_result.append(j)
        if len(result) == 20:
            time.sleep(3)
            search(i+1)
    search_result = []
    search(i)
    return search_result

