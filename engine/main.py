"""
                        _oo0oo_
                       o8888888o
                       88" . "88
                       (| -_- |)
                       0\  =  /0
                     ___/`---'\___
                   .' \\|     |// '.
                  / \\|||  :  |||// \
                 / _||||| -:- |||||- \
                |   | \\\  - /// |   |
                | \_|  ''\---/''  |_/ |
                \  .-\__  '-'  ___/-. /
              ___'. .'  /--.--\  `. .'___
           ."" '   `.___\_ | _/___.'  ' "".
          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
          \  \ `_.   \_ __\ /__ _/   .-` /  /
      =====`-.____`.___ \_____/___.-`___.-'=====
                        `=---='


     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

           佛祖保佑       永不宕机     永无BUG
 """

print("""
$$$$$$$\                  $$\             $$\                                           $$$$$$$\            $$\ $$\           
$$  __$$\                 $$ |            $$ |                                          $$  __$$\           \__|$$ |          
$$ |  $$ | $$$$$$\   $$$$$$$ | $$$$$$$\ $$$$$$\    $$$$$$\  $$$$$$$\   $$$$$$\          $$ |  $$ | $$$$$$\  $$\ $$ |$$\   $$\ 
$$$$$$$  |$$  __$$\ $$  __$$ |$$  _____|\_$$  _|  $$  __$$\ $$  __$$\ $$  __$$\         $$ |  $$ | \____$$\ $$ |$$ |$$ |  $$ |
$$  __$$< $$$$$$$$ |$$ /  $$ |\$$$$$$\    $$ |    $$ /  $$ |$$ |  $$ |$$$$$$$$ |        $$ |  $$ | $$$$$$$ |$$ |$$ |$$ |  $$ |
$$ |  $$ |$$   ____|$$ |  $$ | \____$$\   $$ |$$\ $$ |  $$ |$$ |  $$ |$$   ____|        $$ |  $$ |$$  __$$ |$$ |$$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$\ \$$$$$$$ |$$$$$$$  |  \$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$\         $$$$$$$  |\$$$$$$$ |$$ |$$ |\$$$$$$$ |
\__|  \__| \_______| \_______|\_______/    \____/  \______/ \__|  \__| \_______|$$$$$$\ \_______/  \_______|\__|\__| \____$$ |
                                                                                \______|                            $$\   $$ |
                                                                                                                    \$$$$$$  |
                                                                                                                     \______/ """)

import os
import generator
import json
import time

from bilibili_api import Credential

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('config/credential.txt', 'r', encoding='utf-8') as f:
    text = f.read().split('\n')
credential = Credential('text[1]', 'text[3]')
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
with open('config/weight_map.json', 'r', encoding='utf-8') as f:
    weight_map = json.load(f)
time_1 = time.time()
videos = generator.get_today_video(credential, config, weight_map)
generator.write_video_info(generator.sort_video(videos))
generator.update_database_list()
time_2 = time.time()
print('程序已结束,耗时', time_2 - time_1, '秒')
with open('count.txt', 'r', encoding='utf-8') as f:
    try:
        count = int(f.read()) + 1
    except:
        count = 1

with open('count.txt', 'w', encoding='utf-8') as f:
    f.write(str(count))