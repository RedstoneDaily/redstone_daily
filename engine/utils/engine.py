decorated_functions = []


def hook(func):
    """
    用于注册获取新闻时需要执行的函数, 获取新闻时只需要在函数上添加 @engine_hook 装饰器即可被统一执行
    """
    decorated_functions.append(func)
    return func


def executor(*args, **kwargs):
    """
    执行被注册的函数
    """
    results = []
    for func in decorated_functions:
        result = func(*args, **kwargs)
        results.append(result)
    return results


if __name__ == '__main__':
    executor()
