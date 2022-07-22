# 青龙脚本

## 介绍
一些青龙面板的有趣脚本

### mrrs.py

名称：每日热点

拉取：ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/mrrs.py

配置：无

定时：8 8 * * *（每天一次即可）

### smzdm.py

名称：什么值得买爆料

拉取：ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/smzdm.py

配置：变量smzm_key为爆料关键字，如"小米K50"

定时：8 8 * * *（每天一次即可）

### nwct.py（已废弃）

名称：青龙外网访问

拉取：ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/nwct.py

配置：变量qlsubdomain为域名前缀，建议首次手动运行一次任务，再查看任务日志

定时：*/10 * * * *（建议10分钟）

### getip.py

名称：获取公网IP地址

拉取：ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/getip.py

配置：无

定时：* 8 * * 6（自定义）

### 链接
[python-ngrok](https://github.com/hauntek/python-ngrok)
[open-dingtalk](https://github.com/open-dingtalk/pierced)