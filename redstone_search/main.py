import asyncio
import json
import random, shutil, cv2

from bilibili_api import video, Credential, HEADERS
import httpx
import os
from tqdm import tqdm
from PIL import Image

async def download_url(url, out):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in tqdm(resp.iter_bytes(1024)):
                if not chunk:
                    break

                process += len(chunk)
                f.write(chunk)

async def download_video(bvid = None, aid = None):
    # 实例化 Video 类
    if aid != None:
        v = video.Video(aid = aid)
    elif bvid != None:
        v = video.Video(bvid = bvid)
    else:
        raise ValueError("bvid 或 aid 必须填写一个")
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream() == True:
        # FLV 流下载
        await download_url(streams[0].url, "flv_temp.flv")
        # 转换文件格式
        os.system('ffmpeg -i flv_temp.flv video.mp4')
        # 删除临时文件
        os.remove("flv_temp.flv")
    else:
        # MP4 流下载
        await download_url(streams[0].url, "video_temp.m4s")
        # 转换文件格式
        os.system('ffmpeg -i video_temp.m4s video.mp4')
        # 删除临时文件
        os.remove("video_temp.m4s")

def get_random_frame(bvid = None, aid = None):
    # 尝试删除临时文件
    try:
        os.remove('video.mp4')
    except:
        print("删除临时文件video.mp4失败")

    try:
        os.remove('frame.png')
    except:
        print("删除临时文件frame.png失败")

    try:
        os.system('rmdir /s /q frames')
    except:
        print("删除临时文件夹frames失败")

    # 获取视频
    if aid != None:
        asyncio.get_event_loop().run_until_complete(download_video(aid = aid))
    elif bvid != None:
        asyncio.get_event_loop().run_until_complete(download_video(bvid = bvid))
    else:
        raise ValueError("bvid 或 aid 必须填写一个")

    # 获取随机一帧视频
    # 视频文件名
    input_video = 'video.mp4'

    # 输出图片文件名
    output_image = 'frame.png'

    # 提取所有帧
    # 检测目录是否存在
    if not os.path.exists('frames'):
        os.makedirs('frames')

    # 提取100个切片
    # 获取时长

    cap = cv2.VideoCapture(input_video)  # 打开视频文件
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 获取视频的总帧数
    fps = cap.get(cv2.CAP_PROP_FPS) # 获取帧率
    duration = frame_count / fps # 计算视频时长，单位为秒
    cap.release() # 关闭视频文件
    # 提取帧

    fps = 1/(duration/100) # 计算每秒抽取的帧数
    os.system(f'ffmpeg -i {input_video} -vf fps={fps} frames/frame%04d.png')

    # 随机选择一帧
    frame_list = os.listdir('frames')
    print(frame_list)
    random_frame = random.choice(frame_list)
    print(random_frame)

    # 复制到输出文件
    shutil.copyfile(os.path.join('frames', random_frame), output_image)

    # 删除临时文件
    try:
        os.system('rmdir /s /q frames')
    except:
        print("删除临时文件夹frames失败")

    try:
        os.remove('video.mp4')
    except:
        print("删除临时文件video.mp4失败")

def get():
    videos = []
    # 读取数据库
    with open("../engine/data/database_list.json") as list:
        files = json.load(list)
        for file in files:
            with open("../engine/data/database/" + file["date"] + ".json", "r", encoding="utf-8") as f:
                for video in json.load(f)["content"]:
                    videos.append(int(video["url"].split("av")[1]))

    # 随机选择一个视频
    aid = random.choice(videos)
    get_random_frame(aid = aid)

    # 切割帧(主要是切割UP水印)

    with Image.open('frame.png') as img:
        # 获取图片的宽度和高度
        width, height = img.size

        # 计算裁剪的边界
        left = width * 0.2  # 左边裁剪10%
        top = height * 0.2  # 上边裁剪10%
        right = width * 0.8  # 右边保留90%
        bottom = height * 0.8  # 下边保留90%

        # 裁剪图片
        cropped_img = img.crop((left, top, right, bottom))

        # 显示裁剪后的图片
        cropped_img.show()

        # 保存裁剪后的图片
        cropped_img.save('cropped.png')

    # 尝试删除临时文件
    try:
        os.remove('frame.png')
    except:
        print("删除临时文件frame.png失败")

if __name__ == '__main__':
    get()

