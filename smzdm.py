# -*- coding: UTF-8 -*-
# Version: v1.3
# Created by lstcml on 2022/05/27

import os
import re
import sys
import requests
import datetime

'''
v1.1更新记录：
1、新增脚本自动更新
2、新增默认按价格升序

v1.2更新记录：
1、修复关键字错误
2、修复推送失败

v1.3更新记录：
1、修复推送逻辑
'''

# 更新检测
def checkUpdate():
    print("当前运行的脚本版本：" + str(version))
    try:
        r1 = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/smzdm.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/smzdm.py &")
    except:
        pass

# 获取爆料信息
def getInfo(key, pages):
    try:
        _dict = {}
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
                _dict[_content] = price
        for i in dict(sorted(_dict.items(), key=lambda x: x[1])):
            content = content + i
        return content
    except:
        return ''

# 推送
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)
    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False


if __name__ == '__main__':
    version = 1.3
    checkUpdate()
    try:
        smzdm_key = os.environ["smzdm_key"]
    except:
        smzdm_key = ''
    try:
        smzdm_pages = os.environ['smzdm_pages']
    except :
        smzdm_pages = '1'

    if smzdm_key != '' and smzdm_pages != '':
        if load_send():
            content = getInfo(smzdm_key, smzdm_pages)
            if content != '':
                print('获取“%s”爆料成功！' % smzdm_key)
                send("什么值得买“%s”爆料" % smzdm_key, datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S") + '：\n' + content)
            else:
                print('获取“%s”爆料失败！' % smzdm_key)
    else:
        print('请添加监控关键字变量：smzdm_key！')