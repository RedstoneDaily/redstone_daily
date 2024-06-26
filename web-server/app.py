import asyncio
import io
import json
import os
import time
from pathlib import Path
from urllib.parse import *

import yaml
from flask import *
from flask_cors import CORS
from markupsafe import escape
from pymongo import MongoClient

from redstonesearch import main as rssget
from redstonesearch import test as rsstest

os.chdir(Path(__file__).parent.parent)  # 切换工作目录到仓库根目录
pages_dir = Path.cwd().parent / "frontend"  # 前端仓库目录
pages_flutter_dir = pages_dir / "flutter_project" / "build" / "web"  # Flutter页面目录
pages_vue_dir = pages_dir / "vue"  # Vue页面目录

# 读取配置文件 config.yml
with open(Path(__file__).parent / 'config.yml', 'r') as f:
    config = yaml.safe_load(f)

# 连接数据库
# TODO: Exception handling
db_config = config.get('db')
client = MongoClient(db_config['host'], db_config['port'])
db = client[db_config['name']]
daily = db['daily']  # 今日数据


app = Flask(__name__)
# CORS(app, origins=["http://localhost:18042"])
# CORS(app, origins=["http://120.27.231.122"])
CORS(app)


# 异步任务运行函数
def asyncio_wrapper(job):
    """
    异步任务运行函数，用于运行异步任务。

    参数:
    :param job:
        异步任务函数。
    :return:
        异步任务函数的运行结果。
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as ex:
        print(ex)
        loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(job)
    finally:
        loop.close()


def send_from_directory_cdn_proxied(
        directory: str,
        path: str,
        **kwargs):
    """
    通过 CDN 代理发送文件。

    该函数将检查全局 `config` 对象,以确定是否启用了 CDN。
    如果启用,它将将请求重定向到 CDN URL。
    否则,它将使用 `send_from_directory` 直接提供该文件。

    参数:
        filename (str): 要发送的文件名。
        directory (str, optional): 包含该文件的目录。默认为 'static'。
        **kwargs: 传递给 `send_from_directory` 的其他关键字参数。

    返回:
        一个 Flask 响应对象。
    """

    try:

        # Get the CDN configuration
        cdn_config = config.get("cdn", {})
        cdn_enabled = cdn_config.get("enabled", False)
        src_fs_base = Path(cdn_config.get("src_fs_base", ".")).resolve()
        p = urlparse(cdn_config.get("dst_url_base"))
        cdn_url_base = urlunsplit((p.scheme, p.netloc, p.path, "", ""))

        # Check if the CDN is enabled
        if cdn_enabled:
            # Construct the CDN URL
            fs_path = (Path(directory) / path).resolve()
            if fs_path.is_relative_to(src_fs_base):
                relative_path = fs_path.relative_to(src_fs_base)
                cdn_url = urljoin(cdn_url_base.rstrip(
                    '/') + '/', str(relative_path))
                # Make a redirect response
                response = redirect(cdn_url, code=302)
                response.headers['Referer'] = request.host_url.rstrip('/')
                return response

    except Exception as ex:
        print(ex)

    # If not possible, serve the file directly
    return send_from_directory(directory, path, **kwargs)


@app.before_request
def before_request():
    # 把https请求重定向到http请求
    if request.url.startswith('https://'):
        url = request.url.replace('https://', 'http://', 1)
        code = 301
        return redirect(url, code=code)


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
    if not all([yy, mm, dd]):  # 检查是否缺少参数
        response = jsonify({"error": "missing parameters"})
        response.status_code = 400
        return response

    if len(yy) != 4 or len(mm) != 2 or len(dd) != 2:  # 检查参数格式是否正确
        response = jsonify({"error": "invalid parameters"})
        response.status_code = 400
        return response
    # 对输入的年月日进行转义，防止注入攻击
    y = escape(yy)
    m = escape(mm)
    d = escape(dd)

    # 将转义后的年月日拼接成日期字符串
    date_string = y + '-' + m + '-' + d

    # 打开并读取数据库

    data = daily.find_one({'title': date_string})  # 获取数据列表
    print(data)

    if data is None:
        # 如果未找到对应日期的数据，则返回404错误
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    del data['_id']  # 删除MongoDB自动添加的_id字段
    return jsonify(data)  # 返回数据列表


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
    keyword = escape(keyword)  # 转义关键词，防止注入攻击

    res = []  # 初始化搜索结果列表

    # 打开并读取数据库

    data = daily.find()

    if data is None:
        # 如果未找到最新日报，则返回404错误
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    count = 0  # 记录搜索结果数量
    # 遍历数据库列表，加载每个数据库的视频信息
    for video_data in data:
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
    - start: 起始日期，字符串yyyy-mm-dd格式
    - stop: 结束日期，字符串yyyy-mm-dd格式

    返回值:
    - 如果找到对应日期的数据，则以JSON格式返回数据。
    - 如果未找到对应日期的数据，则返回一个包含错误信息的JSON，状态码为404。
    """
    # 获取参数
    start = request.args.get('start', type=str)
    stop = request.args.get('stop', type=str)

    # 处理参数
    if stop is None:
        stop = start

    # 处理参数格式
    start_date = start.split('-')
    stop_date = stop.split('-')
    # 打开并读取数据库

    database = daily.find()

    if database is None:
        # 如果未找到日报列表，则返回404错误
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    data = []  # 初始化数据列表

    for i in database:
        data.append(i['title'])  # 取出日期字段

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
    # 打开并读取数据库

    data = daily.find()

    if data is None:
        # 如果未找到日报列表，则返回404错误
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    res = []  # 初始化结果列表

    for i in data:
        # 取出日期字段和标题字段
        res.append({"date": i['title'], "title": i['content'][0]['title']})

    return jsonify(res)  # 返回日报列表


@app.route('/api/latest')
def latest():
    """
    获取最新日报。
    返回值:
    返回一个包含最新日报的JSON响应。
    """
    # 打开并读取数据库

    data = daily.find().sort('_id', -1).limit(1).next()

    if data is None:
        # 如果未找到最新日报，则返回404错误
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response

    del data['_id']  # 删除MongoDB自动添加的_id字段
    return jsonify(data)  # 返回最新日报


@app.route('/api/redstonesearch')
def redstonesearch():
    """
    红石图寻
    :return:
    """

    # 主函数
    def main():
        # 调用异步函数获取图片
        image = asyncio_wrapper(rssget.get())

        # 保存图片到内存
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        # 标记当前请求并未进行
        with open('tempconfig.json', 'r') as f:
            config = json.load(f)
            config['is_running']['redstonesearch'] = False
            with open('tempconfig.json', 'w') as f:
                json.dump(config, f)

        # 返回一个 Response 对象，包含图像的字节流
        return Response(img_io, mimetype='image/png')

    # 强制执行
    try:
        if request.args.get('force', type=int) == 1:
            time.sleep(100)
            main()
    except:
        pass

    # 检测是否有其他请求正在进行
    with open('tempconfig.json', 'r') as f:
        config = json.load(f)
        if config['is_running']['redstonesearch']:
            response = '错误：其他请求正在进行，请稍后再试。或强制执行，但因带宽原因，速度可能受限。'
            response.status_code = 400
            return response

    # 标记当前请求正在进行
    with open('tempconfig.json', 'r') as f:
        config = json.load(f)
        config['is_running']['redstonesearch'] = True
        with open('tempconfig.json', 'w') as f:
            json.dump(config, f)

    main()


@app.route('/api/redstonesearch/test')
def redstonesearch_test():
    """
    红石图寻相似度测试
    :return:
    返回值:
    返回源视频和目标视频的相似度。
    """
    # 获取参数
    source_url = request.args.get('source')
    target_url = request.args.get('target')

    return str(rsstest.test(source_url, target_url))


# Vue页面，放在/vue下
@app.route('/vue', methods=['GET'])
def index_vue():
    """
    也是首页
    """
    return send_file(pages_vue_dir / 'index.html')


@app.route("/vue/<path:filename>", methods=['GET'])
# Vue页面资源
def res_vue(filename):
    return send_from_directory_cdn_proxied(pages_vue_dir, filename, as_attachment=False)


@app.route('/', methods=['GET'])
# Flutter页面，放在/下
def index():
    """
    首页
    """
    return send_file(pages_flutter_dir / 'index.html')


@app.route("/<path:filename>", methods=['GET'])
# Flutter页面资源
def res(filename):
    return send_from_directory_cdn_proxied(pages_flutter_dir, filename, as_attachment=False)


app.run(debug=True)
