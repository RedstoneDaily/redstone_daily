from cachetools import LRUCache, cached
from engine.config import config
from engine.data.database import get_database


class News:
    def __init__(self, news_collection='news', item_collection='news_items'):
        self.news_database = get_database().set_collection(news_collection)
        self.item_database = get_database().set_collection(item_collection)

    def get_item(self, doc: dict) -> list:
        """
        从id链接获取新闻内容
        :param doc: 新闻文档
        :return: 新闻内容
        """
        content = []
        for item_index in doc['items']:
            item_doc = self.item_database.find_one({"id": item_index})
            content.append(item_doc)

        return content

    @cached(LRUCache(maxsize=config.cache_ratio * 8))
    def get_news_by_date(self, date: str) -> list:
        """
        根据日期获取新闻内容
        :param date: 日期
        :return: 新闻内容
        """
        doc = self.news_database.find_one({"date": date})

        if doc:
            return self.get_item(doc)

        return []


if __name__ == '__main__':
    # 测试用例
    news = News()
    news_item = news.get_news_by_date('test_date')
    print(news_item)