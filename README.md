# REDSTONE_DAILY

## 项目介绍

红石日报Redstone Daily是一个开源非盈利的网站项目，收集跟进全网红石科技的最新前沿进展，并以日报、周报、月报以及年报的形式发布， 还有搜索功能可以搜索指定内容进行搜索。

## 项目组成

### engine: 用于生成日报数据的引擎

使用engine中的代码可以进行数据的爬取和自动化筛选和储存，参考[这里](engine/README.md)

### webserver: 用于展示日报数据的后端flask框架

webserver用于网页的展示，以及API用于前端获取日报信息，参考[这里](webserver/README.md)