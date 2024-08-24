import os
from datetime import datetime, timedelta

from flask import Flask, request, jsonify

from engine.utils.data.news import news

app = Flask(__name__)


@app.route('/daily/get/<date>')
def daily(date):
    """
    根据日期获取当日的新闻
    :param date: 日期,YYYY-MM-DD
    :return: List[Dict]
    """

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

    return jsonify(news.get_news_by_date_range(start, end))


@app.route('/daily/')
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