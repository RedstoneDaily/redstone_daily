import os

from flask import Flask, request, jsonify

from engine.utils.data.news import news

app = Flask(__name__)


@app.route('/daily/<date>')
def daily(date):

    news_ = news.get_news_by_date(date)
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/latest')
def latest():
    news_ = news.get_latest()
    response_ = []

    for i in news_:  # 删除MongoDB自动添加的_id字段
        del i['_id']
        response_.append(i)

    return jsonify(response_)


@app.route('/search/<query>')
def search(query):
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