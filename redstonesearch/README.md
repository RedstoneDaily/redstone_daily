# redstone-search

redstone-search红石图寻提供一张随机红石图片, 用户可以寻找这张图片的出处并对相似性进行评分。

## 目录结构

```
.
├── README.md
├── init.py # 程序入口文件
├── main.py # 程序主体文件
└── test.py # 相似度测试文件
```

## main.py

从数据库中随机选取一张红石图片

### download_url(url, out)

下载视频网址对应的视频文件到本地
参数:
- url: string, 视频网址
- out: string, 本地保存路径

返回值:
无

### async def download_video(bvid = None, aid = None)

下载视频
参数:
- bvid: string, 视频BV号
- aid: string, 视频AV号
#### 注意: bvid和aid必须选填其中一个

返回值:
无

### get_random_frame(bvid = None, aid = None)

获取随机一帧视频
参数:
- bvid: string, 视频BV号
- aid: string, 视频AV号
#### 注意: bvid和aid必须选填其中一个

返回值:
无

### get(bvid = None, aid = None)

获取随机一张红石图片
参数:
- bvid: string, 视频BV号
- aid: string, 视频AV号
#### 注意: bvid和aid必须选填其中一个

返回值:
无

## test.py

测试相似度算法

### smart_detection(text)

智能检测输入并格式化为aid/bvid
参数:
- text: string, 输入文本

返回值:
dict, 结构为:
```
{
    "type": string, "aid / bvid",
    "value": int, 值
}
```

### test(link, source)

测试相似度算法
参数:
- link: string, 视频链接
- source: string, 需要检测的视频来源

返回值:
score: int, 相似度分数

