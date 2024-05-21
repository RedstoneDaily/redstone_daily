import os
from pathlib import Path
from flask import send_file, send_from_directory, redirect
from flask import Flask, jsonify, request
from flask_cors import CORS
from markupsafe import escape
import json

os.chdir(Path(__file__).parent.parent)  # 切换工作目录到仓库根目录
pages_dir = Path.cwd().parent / "frontend" # 前端页面目录

app = Flask(__name__)
# CORS(app, origins=["http://localhost:18042"])
# CORS(app, origins=["http://120.27.231.122"])
CORS(app)

# 把https请求重定向到http请求
@app.before_request
def before_request():
    if request.url.startswith('https://'):
        url = request.url.replace('https://', 'http://', 1)
        code = 301
        return redirect(url, code=code)

# 重定向字体文件
@app.route('/assets/assets/fonts/FontquanXinYiGuanHeiTi-Regular.ttf')
def redirect_font():
    return redirect('https://aka.redstonedaily.top/assets/assets/fonts/FontquanXinYiGuanHeiTi-Regular.ttf', code=302)

@app.route('/api/daily')
def user_page():
    """
    根据给定的年月日，返回对应日期的数据。

    参数:
    - yy: 年份，字符串格式
    - mm: 月份，字符串格式
    - dd: 日，字符串格式

    返回值:
    - 如果找到对应日期的数据，则以JSON格式返回数据。
    - 如果未找到对应日期的数据，则返回一个包含错误信息的JSON，状态码为404。
    """
    yy = request.args.get('yy', type=str)
    mm = request.args.get('mm', type=str)
    dd = request.args.get('dd', type=str)
    if not all([yy, mm, dd]):# 检查是否缺少参数
        response = jsonify({"error": "missing parameters"})
        response.status_code = 400
        return response

    if len(yy)!= 4 or len(mm)!= 2 or len(dd)!= 2:  # 检查参数格式是否正确
        response = jsonify({"error": "invalid parameters"})
        response.status_code = 400
        return response
    # 对输入的年月日进行转义，防止注入攻击
    y=escape(yy)
    m=escape(mm)
    d=escape(dd)

    # 将转义后的年月日拼接成日期字符串
    date_string = y + '-' + m + '-' + d

    # 打开并读取数据列表文件
    with open('engine/data/database_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 遍历数据列表，查找匹配的日期
    for i in data:
        if i["date"] == date_string:
            # 打开并读取对应日期的数据文件
            with open('engine/data/database/' + date_string + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return jsonify(data)  # 找到匹配日期，返回数据

    # 未找到匹配日期，返回错误信息
    response = jsonify({"error": "not found"})
    response.status_code = 404
    return response

@app.route('/api/search/<keyword>')
def search(keyword):
    """
    根据提供的关键词搜索视频信息。

    参数:
    - keyword: 用户输入的搜索关键词。

    返回值:
    - 返回一个包含搜索结果的列表（无结果则返回空列表）
    """
    page = request.args.get('page', type=int, default=1)
    keyword=escape(keyword)  # 转义关键词，防止注入攻击

    res = []  # 初始化搜索结果列表

    # 从json文件中加载数据库列表
    with open('engine/data/database_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0  # 记录搜索结果数量
    # 遍历数据库列表，加载每个数据库的视频信息
    for i in data:
        with open('engine/data/database/' + i + '.json', 'r', encoding='utf-8') as f:
            video_data = json.load(f)

            # 在每个视频的信息中搜索关键词
            for j in video_data['content']:
                if keyword in j['title'] or keyword in j['description']:
                    count += 1  # 记录搜索结果数量
                    if count <= (page - 1) * 30:  # 如果当前搜索结果数量小于当前页码乘以每页显示数量，则跳过当前视频
                        continue
                    elif count > page * 30:  # 如果当前搜索结果数量大于等于当前页码乘以每页显示数量，则跳出循环
                        break
                    res.append(j)  # 如果关键词匹配，则将视频信息添加到结果列表

    # 如果没有找到匹配的视频信息，则返回404错误
    if len(res) == 0:
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    return res  # 返回搜索结果列表

@app.route('/api/query/')
def query():
    """
    根据给定的起止日期，返回对应日期的数据。

    参数:
    - start: 起始日期，字符串格式
    - stop: 结束日期，字符串格式

    返回值:
    - 如果找到对应日期的数据，则以JSON格式返回数据。
    - 如果未找到对应日期的数据，则返回一个包含错误信息的JSON，状态码为404。
    """
    start = request.args.get('start', type=str)
    stop = request.args.get('stop', type=str)

    if stop is None:
        stop = start

    start_date = start.split('-')
    stop_date = stop.split('-')
    # 打开并读取数据列表文件
    with open('engine/data/database_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    res = []  # 初始化搜索结果列表
    # 遍历数据列表，查找匹配的日期
    for i in data:
        y, m, d = i.split('-')
        if int(start_date[0]) <= int(y) <= int(stop_date[0]):
            if int(start_date[1]) <= int(m) <= int(stop_date[1]):
                if int(start_date[2]) <= int(d) <= int(stop_date[2]):
                    res.append(i)

    return jsonify(res)  # 返回搜索结果列表

@app.route('/api/list')
def list():
    """
    获取日报列表。
    返回值:
    - 如果找到日报列表，则返回一个包含日报列表的JSON响应。
    """
    # 打开并读取数据列表文件
    with open('engine/data/database_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)  # 返回日报列表

@app.route('/api/latest')
def latest():
    """
    获取最新日报。
    返回值:
    返回一个包含最新日报的JSON响应。
    """
    # 打开并读取数据列表文件
    with open('engine/data/database_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    latest_date = data[-1]["date"]  # 获取最新日报日期

    # 打开并读取最新日报数据文件
    with open('engine/data/database/' + latest_date + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)  # 返回最新日报数据
@app.route('/', methods=['GET'])
def index():
    """
    首页
    """
    return send_file(pages_dir / 'index.html')

@app.route("/<path:filename>", methods=['GET'])
def res(filename):
    directory = f"{pages_dir}"  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=False)

app.run(ssl_context='adhoc')