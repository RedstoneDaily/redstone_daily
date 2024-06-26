from io import BytesIO

import json
import requests
import time
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

font80 = ImageFont.truetype('font.otf', 80)
font50 = ImageFont.truetype('font.otf', 50)
font40 = ImageFont.truetype('font.otf', 40)
font35 = ImageFont.truetype('font.otf', 35)
font30 = ImageFont.truetype('font.otf', 30)
font20 = ImageFont.truetype('font.otf', 20)


def print_daily():
    def download_and_paste_image(url, img, x, y, width, height):
        """
        从URL下载图片，缩放到指定尺寸，并粘贴到目标图片img的(x, y)位置。

        :param url: 图片的URL
        :param img: 目标Pillow Image对象
        :param x: 粘贴位置的横坐标
        :param y: 粘贴位置的纵坐标
        :param width: 缩放后的图片宽度
        :param height: 缩放后的图片高度
        """
        # 发送HTTP请求下载图片
        response = requests.get("https:" + url)
        response.raise_for_status()  # 检查请求是否成功

        # 从响应内容中读取图片数据并创建Pillow Image对象
        with BytesIO(response.content) as image_file:
            downloaded_img = Image.open(image_file)

            # 缩放图片到指定尺寸
            resized_img = downloaded_img.resize((width, height))
        # 将缩放后的图片粘贴到目标图片上
        img.paste(resized_img, (x, y))

        # 先读取今日的数据

    filename = './data/database/' + time.strftime("%Y-%m-%d", time.localtime()) + '.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    # 判断需要的画布大小
    width = 1000
    length = len(data["content"])
    if length > 3:
        height = 137 * (length - 3) + 694 + 25
    elif length > 2:
        height = 694 + 25
    elif length > 1:
        height = 500 + 25
    else:
        height = 316 + 25

    # 记得加上头图的高度
    height += 150

    # 创建画布
    img = Image.new('RGB', (width, height), (255, 255, 255))

    draw = ImageDraw.Draw(img)

    # 现在height变成当前y坐标哩
    height = 0

    # 加上头图
    img.paste(Image.open('./images/head.png'), (0, height))
    height += 150 + 25

    for i in tqdm(range(length)):
        if i == 0:
            # 绘制头条内容
            download_and_paste_image(data["content"][i]["cover_url"], img, 25, height, 500, 281)
            draw.polygon([(25, height + 281 - 100 - 1), (25, height + 281 - 1), (25 + 100, height + 281 - 1)],
                         fill='#740000')
            draw.polygon([(25 + 500, height + 100), (25 + 500, height), (25 + 500 - 100, height)], fill='#740000')
            draw.rectangle([(25 + 500, height), (1000 - 25, height + 100)], fill='#740000')

            draw.text((25 + 500 + 155, height + 10), '今日头条', fill='white', font=font40)
            draw.text((25 + 500 + 260, height + 20), 'Headlines Today', fill='white', font=font30)

            # 标题和简介

            # 标题
            if (len(data["content"][i]["title"]) > 30):
                draw.text((25 + 500 + 10, height + 60), data["content"][i]["title"][:28] + '...', fill='white',
                          font=font40)
            else:
                draw.text((25 + 500 + 10, height + 60), data["content"][i]["title"], fill='white', font=font35)

            draw.text((25 + 5, height + 281 - 100 + 15), '1', fill='white', font=font80)
            draw.text((25 + 30, height + 281 - 100 + 65), 'st', fill='white', font=font30)

            # 简介
            for j in range(0, int(len(data["content"][i]["description"]) / 23) + 1):
                if j > 2:
                    break
                if j == 2 and len(data["content"][i]["description"]) > 125:
                    draw.text((25 + 500 + 10, height + 270), data["content"][i]["description"][100:113] + '...',
                              fill='black', font=font30)
                    break
                draw.text((25 + 500 + 10, height + 110 + j * 33),
                          data["content"][i]["description"][j * 23:(j + 1) * 23], fill='black', font=font30)

            height += 281 + 25
        elif i == 1 or i == 2:
            # 绘制第二三条内容
            download_and_paste_image(data["content"][i]["cover_url"], img, 25, height, 300, 169)
            draw.polygon([(25, height + 169 - 70 - 1), (25, height + 169 - 1), (25 + 70, height + 169 - 1)],
                         fill='#740000')
            draw.polygon([(25 + 300, height + 70), (25 + 300, height), (25 + 300 - 70, height)], fill='#740000')
            draw.rectangle([(25 + 300, height), (1000 - 25, height + 70)], fill='#740000')

            # 标题
            if i == 1:
                draw.text((25 + 5, height + 169 - 50 + 7), '2', fill='white', font=font40)
                draw.text((25 + 27, height + 169 - 50 + 27), 'nd', fill='white', font=font20)
            if i == 2:
                draw.text((25 + 5, height + 169 - 50 + 7), '3', fill='white', font=font40)
                draw.text((25 + 27, height + 169 - 50 + 27), 'rd', fill='white', font=font20)
            if (len(data["content"][i]["title"]) > 19):
                draw.text((25 + 300 + 10, height + 10), data["content"][i]["title"][:17] + '...', fill='white',
                          font=font50)
            else:
                draw.text((25 + 300 + 10, height + 10), data["content"][i]["title"], fill='white', font=font50)

            # 简介
            for j in range(0, int(len(data["content"][i]["description"]) / 33) + 1):
                if j > 2:
                    break
                if j == 2 and len(data["content"][i]["description"]) > 99:
                    draw.text((25 + 300 + 10, height + 141), data["content"][i]["description"][66:97] + '...',
                              fill='black', font=font30)
                    break
                draw.text((25 + 300 + 10, height + 75 + j * 33),
                          data["content"][i]["description"][j * 33:(j + 1) * 33 - 1], fill='black', font=font30)

            height += 169 + 25
        else:
            # 剩下的
            download_and_paste_image(data["content"][i]["cover_url"], img, 25, height, 200, 112)
            draw.polygon([(25 + 200, height + 50), (25 + 200, height), (25 + 200 - 50, height)], fill='#740000')
            draw.rectangle([(25 + 200, height), (1000 - 25, height + 50)], fill='#740000')

            # 标题
            if len(data["content"][i]["title"]) > 39:
                draw.text((25 + 200 + 10, height + 10), data["content"][i]["title"][:38] + '...', fill='white',
                          font=font30)
            else:
                draw.text((25 + 200 + 10, height + 10), data["content"][i]["title"], fill='white', font=font30)

            # 简介
            for j in range(0, int(len(data["content"][i]["description"]) / 63) + 1):
                if j > 1:
                    break

                if j == 1 and len(data["content"][i]["description"]) > 126:
                    draw.text((25 + 200 + 10, height + 80), data["content"][i]["description"][63:124] + '...',
                              fill='black', font=font20)
                    break
                draw.text((25 + 200 + 10, height + 55 + j * 25), data["content"][i]["description"][j * 64:(j + 1) * 63],
                          fill='black', font=font20)

            height += 112 + 25

    # 显示日期
    with open('count.txt', 'r', encoding='utf-8') as f:
        count = f.read()
    draw.text((700, 100), '[' + time.strftime("%Y-%m-%d", time.localtime()) + ' #' + str(count) + ']', fill='white',
              font=font40)

    # 输出到./data/output
    img.save('./data/output/' + time.strftime("%Y-%m-%d" + '.png'))


print_daily()
