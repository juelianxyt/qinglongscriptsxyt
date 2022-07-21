# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2022/04/26
# 建议定时10分钟：*/10 * * * *
'''
指定分享目录：不设置默认为脚本路径，可以通过变量chfs_path指定目录，格式：/ql/scripts，避免误操作导致青龙无法启动，建议使用默认值；
设置账户密码：不设置默认为qinglong/123456，可以通过变量chfs_up指定目录，格式：账号:密码（admin:123456），注意此处为英文冒号；
'''
import os
import socket
import requests
from time import sleep

def update():
    print("当前运行的脚本版本：" + str(version ))
    try:
        r1 = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/chfs.py").text
        r2 = re.findall(re.compile("version = \d.\d"),r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/chfs.py &")
    except:
        pass

def download_chfs():
    if not os.path.exists("/bin/chfs"):
        print("检测到主程序不存在，正在下载主程序...")
        os.system("git clone https://gitee.com/lstcml/qinglongscripts.git /tmp/chfs>/dev/null 2>&1 && tar zxf /tmp/chfs/chfs.tar.gz -C /bin && rm -rf /tmp/chfs* && chmod +x /bin/chfs")
    start_chfs()

def process_daemon(command):
    url = "http://" + get_host_ip() + ":5900"
    webdav = url + "/webdav"
    n = os.popen("ps -ef | grep 'chfs'").read()
    if chfs_path not in n:
        os.system(command + ">/dev/null 2>&1 &")
        n = os.popen("ps -ef | grep 'chfs'").read()
        if chfs_path not in n:
            print("启动chfs失败.")
            return False
        else:
            print("启动chfs成功.\n访问地址：" + url + "\nWebdav：" + webdav)
            return True
    else:
        print("chfs已运行中.\n访问地址：" + url + "\nWebdav：" + webdav)
        return True

def start_chfs():
    print("正在启动chfs.")
    command = 'chfs --log=/tmp/ --path="' + chfs_path + '" --port=5900 --rule="::|' + chfs_up + ':rwd"'
    if not process_daemon(command):
        os.system("kill -9 `ps -ef | grep 'chfs' | grep -v 'grep' | awk '{print $1}'`")
        sleep(3)
        os.system(command + ">/dev/null 2>&1 &")
        sleep(3)
        process_daemon(command)

# 查询本机ip地址
def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    version = 1.0
    update()
    # 设置用户与密码
    try:
        chfs_up = os.environ["chfs_up"]
    except:
        print("检测到未设置账号，已启用默认账号密码：qinglong/123456")
        chfs_up = "qinglong:123456"
    tmp = chfs_up.split(":")
    if len(tmp) != 2:
        print("chfs_up变量设置错误！已启用默认用户名密码为：qinglong/123456")
        chfs_up = "qinglong:123456"
   
        # 指定分享目录
    try:
        chfs_path = os.environ["chfs_path"]
    except:
        if os.path.exists("/ql/scripts"):
            chfs_path = "/ql/scripts"
        else:
            chfs_path = "/ql/data/scripts"
    if chfs_path[0] != "/":
        print("chfs_path变量设置错误！")
    else:
        download_chfs()
