import asyncio
import random, shutil, cv2

from bilibili_api import video, Credential, HEADERS
import httpx
import os
from tqdm import tqdm

async def download_url(url: str, out: str, info: str):
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

async def download_video(bvid: str):
    # 实例化 Video 类
    v = video.Video(bvid = bvid)
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream() == True:
        # FLV 流下载
        await download_url(streams[0].url, "flv_temp.flv", "FLV 音视频流")
        # 转换文件格式
        os.system('ffmpeg -i flv_temp.flv video.mp4')
        # 删除临时文件
        os.remove("flv_temp.flv")
    else:
        # MP4 流下载
        await download_url(streams[0].url, "video_temp.m4s", "视频流")
        # 转换文件格式
        os.system('ffmpeg -i video_temp.m4s video.mp4')
        # 删除临时文件
        os.remove("video_temp.m4s")

def get_random_frame():
    bvid="BV1MVKaebEqA"
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
    asyncio.get_event_loop().run_until_complete(download_video(bvid))

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
    os.remove('video.mp4')


if __name__ == '__main__':
    # 主入口
    get_random_frame()