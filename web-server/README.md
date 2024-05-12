# webserver

红石日报的后端脚本, 使用 Python Flask 框架开发, 主要提供api接口.

## 目录结构

```
├── app.py  # 主程序
```

## app.py

主脚本.

### @app.route('/api/daily')

根据给定的年月日，返回对应日期的数据。

参数:
- yy: 年份，字符串格式
- mm: 月份，字符串格式
- dd: 日，字符串格式

返回值:
- 如果找到对应日期的数据，则以JSON格式返回数据。
- 如果未找到对应日期的数据，则返回一个包含错误信息的JSON，状态码为404。

### @app.route('/api/search/<keyword>')

根据提供的关键词搜索视频信息。

参数:
- keyword: 用户输入的搜索关键词。

返回值:
- 如果找到相关视频信息，则返回一个包含搜索结果的列表。
- 如果未找到相关视频信息，则返回一个包含错误信息的JSON响应。

### @app.route('/api/query/')

根据给定的起止日期，返回对应日期的数据。

参数:
- start: 起始日期，字符串 yyyy-mm-dd 格式
- stop: 结束日期，字符串 yyyy-mm-dd 格式

返回值:
- 如果找到对应日期的数据，则以JSON格式返回数据。
- 如果未找到对应日期的数据，则返回一个包含错误信息的JSON，状态码为404。

### @app.route('/api/list')

获取日报列表。
返回值:
- 如果找到日报列表，则返回一个包含日报列表的JSON响应。

### @app.route('/api/lastest')

获取最新一期日报。
返回值:
- 一个包含最新一期日报的JSON响应。

### @app.route('/', methods=['GET'])

主页。

### @app.route("/<path:filename>", methods=['GET'])

静态文件服务。