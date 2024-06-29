# engine

## 简介

engine用于处理日报的实现, 包括生成, 查询, 以及制作其他报纸.

## 目录结构

```
engine/
├── main.py   # 程序入口
├── generator.py  # 日报生成器
├── crawler.py   # 日报爬虫
├── count.txt  # 日报统计文件
├── data/  # 日报数据目录
│   ├── database/
│   │   ├── xxxx-xx-xx.json  # 日报数据文件
│   │   ├── xxxx-xx-xx.json
│   |   └──...
├── config/
│   ├── config.json  # 配置文件
│   └── weight_map.json  # 权重映射文件
```

## main.py

程序入口, 用于启动日报生成器, 爬虫, 以及其他功能.

### 程序功能

- 生成日报: 调用generator.py生成日报

无函数或方法.

## generator.py

日报生成器, 用于调用crawler.py爬取视频, 生成日报. 

### filter_video(title, description, tags, weight_map)

根据权重列表过滤视频数据.
参数:
- title: string, 新闻标题
- description: string, 新闻描述
- tags: list, 新闻标签
- weight_map: dict, 权重映射字典

返回值:
- weight: int, 权重

### calc_score(like, view, favorite, coin, share, review):

计算视频的得分.
参数:
- like: int, 点赞数
- view: int, 播放量
- favorite: int, 收藏量
- coin: int, 硬币数
- share: int, 分享数
- review: int, 评论数

返回值:
- score: int, 得分

### get_today_video(config, weight_map)

获取当日热门视频.
参数:
- config: dict, 配置文件
- weight_map: dict, 权重映射字典

返回值:
- result_list: list, 视频列表

### transform_video_item(video_item: dict) -> dict

将视频数据转换为日报数据.
参数:
- video_item: dict, 视频数据

返回值:
dict, 日报数据

### write_video_info(video_info_list: list[dict])

将日报数据写入json文件.
参数:
- video_info_list: list[dict], 日报数据列表

返回值:
None

### generate_daily_report(config, weight_map)

生成当日日报.
参数:
- config: dict, 配置文件
- weight_map: dict, 权重映射字典

返回值:
None

### update_database_list()

更新数据库列表.
参数:
- None

返回值:
None

## crawler.py 

日报爬虫, 用于从各大新闻网站爬取新闻, 并将其转换为日报数据.

### search_from_bilibili(page, keyword)

搜索B站视频.
参数:
- page: int, 页码
- keyword: string, 关键字

返回值:
- resent_videos: list, 最新视频列表

### def search_video(keyword)

搜索视频.
参数:
- keyword: string, 关键字


返回值:
- search_result: list, 搜索结果

## weight_map.json

权重映射文件, 用于设置视频权重.

文件格式:

```
{
    "terms": ["在任意未知出现时权重乘以1.5, 适合匹配术语", ...],
    "blacklist": [
        "黑名单, 当出现在任意位置时权重置0", ...
    ],
    "weight_map": {
        "global":[
            {"keyword": "关键词", "weight": float,在任意位置出现时的权重},
            ...
        ],
        "special": [
            {
                "keyword": "关键词",
                "title": [float, 在标题出现关键词时的权重, float, 标题没有出现关键词时的权重],
                "description": [float, 在简介出现关键词时的权重, float, 简介没有出现关键词时的权重],
                "tags" : [float, 在标签出现关键词时的权重, float, 标签没有出现关键词时的权重]
            },
            ...
        ]
    }
}
```

## config.json

配置文件, 用于设置程序运行参数.

文件格式:

```
{
    "search": {
        "keyword": "关键词",
        "enable_screening": bool,是否启用筛选
    }
}
```
