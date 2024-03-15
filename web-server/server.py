#coding=utf-8
import os
from pathlib import Path
import sys
from flask import send_file, send_from_directory
from flask import jsonify
from flask import Flask, redirect, request, render_template
import pdb

# 设为True以显示备案过审页面
FOR_REGISTER = False

# Flask apps
app = Flask(__name__)
app_register = Flask("Gallery")

# Paths
engine_dir = Path.cwd() / 'engine'
pages_dir = Path.cwd().parent / "frontend"
gallery_dir = pages_dir / "pages-legacy" / "GalleryDemo"


# app

# @app.route("/download/<filename>", methods=['GET'])
# def download_file(filename):
#     if (filename=='server.py' or filename=='server.log' or filename=='tongji.txt') :
#         return None
#     # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     directory = os.getcwd()  # 假设在当前目录
#     return send_from_directory(directory, filename, as_attachment=True)

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')

# 这个可以不用吗？
@app.route("/daily", methods=['GET'])
def daily_test():
    print("{pages_dir}/index.html")
    return send_file(f"{pages_dir}/index.html")

@app.route("/daily/<path:filename>", methods=['GET'])
def daily_test_res(filename):
    directory = f"{pages_dir}"  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=False)

@app.route("/res/daily/list", methods=['GET'])
def daily_info_list():
    return send_file(f"{engine_dir}/data/database_list.json")

@app.route("/res/daily/<filename>", methods=['GET'])
def daily_info(filename):
    directory = f"{engine_dir}/data/database"  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)

# @app.route('/zh', methods=['GET'])
# def zh():
#     return render_template('indexZH.html')

# @app.route('/en', methods=['GET'])
# def en():
#     return render_template('indexEN.html')

# @app.route("/css/<filename>", methods=['GET'])
# def css(filename):
#     directory = f"{os.getcwd()}/css"  # 假设在当前目录
#     return send_from_directory(directory, filename, as_attachment=True)


# For Registry

@app_register.route('/', methods=['GET'])
def index():
    return send_file(f"{gallery_dir}/GalleryDemo.html")

@app_register.route("/<filename>", methods=['GET'])
def res(filename):
    return send_from_directory(gallery_dir, filename, as_attachment=True)



if __name__ == '__main__':
    # 接受--debug参数则开启debug模式
    if "--debug" in sys.argv:
        app.debug = True
        app_register.debug = True
        
    if FOR_REGISTER:
        app_register.run(host='0.0.0.0',port=80)
    else:
        app.run(host='0.0.0.0',port=80)