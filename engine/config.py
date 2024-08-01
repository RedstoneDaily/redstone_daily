import json
import os


class Config:
    def __init__(self, filename='config.json'):
        # 获取当前文件的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建到"文件目录/config"的路径
        config_dir = os.path.join(base_dir, 'config')
        # 构建配置文件的完整路径
        config_file_path = os.path.join(config_dir, filename)
        # 打开并读取配置文件
        with open(config_file_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

            # 读取配置文件中的参数
            for key, value in self.config.items():
                setattr(self, key, value)


""" 常用配置文件 """

config = Config()
weight_map = Config('weight_map.json')
