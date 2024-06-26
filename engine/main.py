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
                                                                                                                     \______/
"""
import generator
import json
import time

# set cwd
import os
# 更改工作目录到工程根目录的上一级
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#打印工作目录
print("当前工作目录:", os.getcwd())

with open('engine/config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
with open('engine/config/weight_map.json', 'r', encoding='utf-8') as f:
    weight_map = json.load(f)
time_1 = time.time()
videos = generator.get_today_video(config, weight_map)
generator.write_video_info(videos)
generator.update_database_list()
time_2 = time.time()
print('程序已结束,耗时', time_2 - time_1, '秒')
with open('engine/count.txt', 'r', encoding='utf-8') as f:
    try:
        count = int(f.read()) + 1
    except:
        count = 1

with open('engine/count.txt', 'w', encoding='utf-8') as f:
    f.write(str(count))