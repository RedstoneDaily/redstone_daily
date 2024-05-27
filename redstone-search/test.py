from bilibili_api import video, sync
import Levenshtein as lev

def smart_detection(text):
    # 智能检测需要验证的视频URL/BVid格式
    if 'www.bilibili.com' in text and 'av' in text:
        return {"type": "aid", "value": int(text.split('av')[1].split('/')[0])} # 直链, 使用aid
    elif 'www.bilibili.com' in text and 'BV' in text:
        return {"type": "bvid", "value": "BV" + text.split('BV')[1].split('/')[0]} # 分享链接, 使用bvid
    elif 'BV' in text:
        return {"type": "bvid", "value": "BV" + text.split('BV')[1].split('/')[0]} # 直接输入bvid
    elif 'av' in text:
        return {"type": "aid", "value": int(text.split('av')[1].split('/')[0])} # 直接输入aid
    else:
        raise ValueError("无法分析喵: " + text)

def test(link, source):
    # 输入视频链接和源链接
    link = smart_detection(link)
    source = smart_detection(source)


    # 获取视频信息
    if link['type'] == 'aid':
        v = video.Video(aid=link['value'])
    elif link['type'] == 'bvid':
        v = video.Video(bvid=link['value'])

    info = sync(v.get_info())['title']

    if source['type'] == 'aid':
        s = video.Video(aid=source['value'])
    elif source['type'] == 'bvid':
        s = video.Video(bvid=source['value'])

    source_info = sync(s.get_info())['title']

    # 检测两个视频标题相似度评分
    score = lev.distance(info, source_info)

    return score