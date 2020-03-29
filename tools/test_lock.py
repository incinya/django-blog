"""
模拟30个用户瞬间向8000和8001端口随机发请求
"""
import requests
from threading import Thread
import random
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")


# 线程事件函数,功能: 随机向8000和8001 发请求
def get_request():
    url1 = 'http://127.0.0.1:8000/test/'
    url2 = 'http://127.0.0.1:8001/test/'
    url = random.choice([url1, url2])
    # 发请求 - 在浏览器地址栏输入 url ,并且访问
    requests.get(url)


t_list = []

for i in range(30):
    t = Thread(target=get_request)
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()
