import os
import re
from datetime import datetime, timedelta

from flask import Flask, request, jsonify

from engine.utils.data.news import news

app = Flask(__name__)


@app.route('/daily/get/')
def daily_with_no_date():
    return jsonify({'error': '日期参数不能为空, 请检查文档: https://docs.rsdaily.com/api-209738938'}), 422


@app.route('/daily/get/<date>')
def daily(date):
    """
    根据日期获取当日的新闻
    :param date: 日期,YYYY-MM-DD
    :return: List[Dict]
    """

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return jsonify({'error': '日期格式错误, 确保为YYYY-MM-DD格式 文档: https://docs.rsdaily.com/api-209738938'}), 422

    news_ = news.get_news_by_date(date)
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/daily/query')
def query():
    """
    查询两个时间段之间的新闻
    :return: List[Dict]
    """

    start = request.args.get('start_date', None)
    end = request.args.get('end_date', None)

    if start is None or end is None:
        return jsonify({'error': '参数不全或未正确命名, 请检查文档: https://docs.rsdaily.com/api-209740195'}), 422

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', start) or not re.match(r'^\d{4}-\d{2}-\d{2}$', end):
        return jsonify({'error': '日期格式错误, 确保为YYYY-MM-DD格式 文档: https://docs.rsdaily.com/api-209740195'}), 422

    try:
        return jsonify(news.get_news_by_date_range(start, end))
    except ValueError as e:
        if e.args[0] == '时间跨度过长(最大100天)':
            return jsonify({'error': str(e)}), 422


@app.route('/daily')
@app.route('/daily/latest')
def latest():
    """
    获取最新新闻
    :return: List[Dict]
    """
    news_ = news.get_latest()
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/daily/earliest')
def earliest():
    """
    获取最早新闻
    :return: List[Dict]
    """
    news_ = news.get_latest(True)
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/daily/all')
def all():
    """
    获取所有新闻
    :return:
    """

    news_ = news.get_all()
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/search/<query>')
def search(query):
    """
    搜索新闻
    :param query: 搜索关键字
    :return: List[Dict]
    """
    request.args.get('page_count', None)
    request.args.get('page_size', None)
    request.args.get('item_type', None)
    request.args.get('sort', None)
    request.args.get('strictness', None)

    news_ = news.search_item(query)
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


if __name__ == '__main__':
    app.run(debug=True)