from cachetools import LRUCache, cached
from engine.config import config
from engine.utils.data.database import get_database
import time


class News:
    def __init__(self, collection='news_items'):
        self.database = get_database().set_collection(collection)

    def get_item(self, doc: dict) -> list:
        """
        从id链接获取新闻内容
        :param doc: 新闻文档
        :return: 新闻内容
        """
        content = []
        for item_index in doc['items']:
            item_doc = self.database.find_one({"id": item_index})
            content.append(item_doc)

        return content

    @cached(LRUCache(maxsize=config.cache_ratio * 8))
    def get_news_by_date(self, date: str) -> list:
        """
        根据日期获取新闻内容
        :param date: 日期
        :return: 新闻内容
        """

        return self.database.find({"date": date})

    @cached(LRUCache(maxsize=config.cache_ratio * 32))
    def get_item_by_id(self, item_id: int) -> dict:
        """
        根据id获取新闻内容
        :param item_id: 新闻id
        :return: 新闻内容
        """
        doc = self.database.find_one({"id": item_id})

        return doc if doc else {}

    def search_item(self, keyword: str, page_count: int = 1, page_size: int = 20,
                    item_type: str = 'all', sort: str = 'date', strictness: str = 'loose') -> list:
        """
        根据关键字搜索新闻内容
        :param keyword: 关键字
        :param page_count: 页数
        :param page_size: 每页数量
        :param item_type: 新闻类型 可选值: ['all', 'video', 'text']
        :param sort: 排序方式
        date为按发布时间排序, like为按点赞数排序, none不排序
        :param strictness: 严格度
        strictness为完全匹配, 即所有关键词都必须出现在新闻中, 但不限制顺序
        loose为部分匹配, 即部分关键词必须出现在新闻中, 但单个关键词必须完整, 不要求顺序和数量
        regex为正则, 需要用户自己输入表达式
        :return: 新闻内容
        """
        # 检查参数
        if not keyword or not page_count or not page_size or not item_type or not sort or not strictness:
            raise ValueError('传递的一个或多个参数为空')

        if len(keyword) > 100: raise ValueError(f'搜索关键字过长(最大100字): {len(keyword)}')
        if page_count < 1: raise ValueError(f'页数必须大于等于1: {page_count}')
        if page_size < 1: raise ValueError(f'每页数量必须大于等于1: {page_size}')
        if page_size > 100: raise ValueError(f'每页数量过大(最大100): {page_size}')
        if sort not in ['date', 'like', 'none']: raise ValueError(f'排序方式错误: {sort}')
        if strictness not in ['strict', 'loose', 'regex']: raise ValueError(f'严格度参数错误: {strictness}')

        # 构造查询条件
        if strictness == 'strict':
            query = {"$and": [{"title": {"$regex": i, "$options": "i"}} for i in keyword.split(' ')]}
        elif strictness == 'loose':
            query = {"$or": [{"title": {"$regex": i, "$options": "i"}} for i in keyword.split(' ')]}
        elif strictness == 'regex':
            query = {"title": {"$regex": keyword}}

        if 'all' != item_type:
            query['type'] = item_type

        results = self.database.find(query)

        # 排序
        if sort == 'date':
            sorted_results = sorted(results, key=lambda x: x['id'])
        elif sort == 'like':
            sorted_results = sorted(results, key=lambda x: x['data']['like'])
        else:
            sorted_results = results

        return sorted_results[page_size * (page_count - 1): page_size * page_count]


news = News()

if __name__ == '__main__':
    # 测试用例
    _time = time.time()
    news_item = news.get_news_by_date('this_isnt_a_date')
    print(time.time() - _time)

    print(news_item[0]['id'])

    # 测试缓存
    _time = time.time()
    news_item = news.get_news_by_date('test_date')
    print(time.time() - _time)
    print(news_item)

    # 测试搜索
    news_item = news.search_item('test title', page_count=1, page_size=20, item_type='all')  # 部分匹配
    print(f'{news_item}')

    news_item = news.search_item('test title', page_count=1, page_size=20, item_type='all',
                                 strictness='strict')  # 完全匹配
    print(f'{news_item}')

    news_item = news.search_item('test title', page_count=1, page_size=20, item_type='text')  # 新闻类型为text
    print(f'{news_item}')

    news_item = news.search_item('test title', page_count=1, page_size=20, item_type='video')  # 新闻类型为video
    print(f'{news_item}')
