import json
import os


class Config:
    def __init__(self):
        # 获取当前文件的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建config.json的完整路径
        config_file_path = os.path.join(base_dir, 'config.json')
        # 打开并读取配置文件
        with open(config_file_path, 'r') as f:
            self.config = json.load(f)

            # 读取配置文件中的参数
            for key, value in self.config.items():
                setattr(self, key, value)


config = Config()
