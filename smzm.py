# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2022/05/27

import os
import re
import sys
import requests
import datetime

# 获取爆料信息
def getInfo(key, pages):
    try:
        content = ''
        url = 'https://search.smzdm.com/?c=home&s=' + key + '&v=b&p=' + str(pages)
        _headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}
        response = requests.get(url, headers=_headers, data={}).text
        r1 = re.compile(r'<div class="feed-link-btn-inner">((?:.|\n)*?)</div>').findall(response)
        j = 0
        for i in r1:
            j += 1
            r2 = re.compile(r'<a onclick=\";gtmAddToCart((?:.|\n)*?)</a>').findall(i)
            r3 = re.compile(r'[(](.*?)[)]').findall(r2[0])
            keyinfo1 = eval(r3[0])
            keyinfo2 = eval(r3[1].strip("'AddToCart',"))
            price = keyinfo1['metric1']
            name = keyinfo2['article_title']
            buyPlatform = keyinfo2['mall_name']
            url = keyinfo2['go_path']
            if price != 0:
                _content = '<a href=%s>%s %s元 %s</a>\n' % (url, buyPlatform, str(price), name)
            content = content + _content
        return content
    except:
        return ''

# 推送
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
    
    try:
        smzm_key = os.environ["smzm_key"]
    except:
        smzm_key = ''
    try:
        smzm_pages = os.environ['smzm_pages']
    except :
        smzm_pages = '1'

    if smzm_key != '' and smzm_pages != '':
        if load_send():
            content = getInfo(smzm_key, smzm_pages)
            if content != '':
                print('获取“%s”爆料成功！' % smzm_key)
                send("什么值得买“%s”爆料" % smzm_key, datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S") + '：\n' + content)
            else:
                print('获取“%s”爆料失败！' % smzm_key)
    else:
        print('请添加监控关键字变量：smzm_pages！')