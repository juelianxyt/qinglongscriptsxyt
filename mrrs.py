# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2022/05/08
# Crontab：8 8 * * *

import os
import sys
import requests
import datetime
from bs4 import BeautifulSoup

def getNew():
    try:
        url = []
        title = []
        _content = ""
        bdurl = "https://top.baidu.com/board?tab=realtime"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'}

        r = requests.get(bdurl)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')


        for i in soup.find_all(class_="c-single-text-ellipsis"):
            title.append(i.get_text().strip())
        for i in soup.find_all(class_="look-more_3oNWC"):
            url.append(str(i).split("href=\"")[1].split("\"")[0])

        url = list(dict.fromkeys(url))
        for i in range(0, len(title)):
            _content = _content + "<a href=" + url[i] + ">" + title[i] + "</a>\n"
        return _content
    except:
        return ''

def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
            return True
        except:
            print("加载通知服务失败！")
            return False
    else:
        print("加载通知服务失败！")
        return False


if __name__ == '__main__':
    if load_send():
        content = getNew()
        if content != '':
            print('获取今日热点成功！')
            send(datetime.datetime.now().strftime("%Y.%m.%d") + " 今日热点", content)
        else:
            print('获取今日热点失败！')