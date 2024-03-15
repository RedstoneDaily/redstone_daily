import json

from PIL import ImageFont  # 假设你是从PIL库中导入ImageFont


class Font:
    def __init__(self, font_name):
        self.font_name = font_name
        with open("config/fonts.json", "r") as f:
            config = json.load(f)
        self.path = config[self.font_name]["path"]
        self.size = int(config[self.font_name]["size"])

    def get(self, size=30):
        return ImageFont.truetype(self.path, size)
