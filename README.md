# REDSTONE_DAILY

## 项目介绍

红石日报Redstone Daily是一个开源非盈利的网站项目，收集跟进全网红石科技的最新前沿进展，并以日报、周报、月报以及年报的形式发布， 还有搜索功能可以搜索指定内容进行搜索。
(好像是不是混进了什么奇奇怪怪的小工具)

## 项目组成

### engine: 用于生成日报数据的引擎

使用engine中的代码可以进行数据的爬取和自动化筛选和储存，参考[这里](engine_old/README.md)

### webserver: 提供API服务的Flask框架

webserver提供API服务用于前端获取日报信息，文档（TODO）

### redstone-search: 红石图寻: 小游戏

redstone-search提供一张随机红石图片, 用户可以寻找这张图片的出处并对相似性进行评分。（失踪了（?