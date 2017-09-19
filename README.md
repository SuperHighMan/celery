A First celery project
===================================
结合celery开发的一个关于celery的小程序，可用于异步任务的调度。

一、环境要求
-----------------------------------
本程序基于Python3开发，推荐>=Python3.5，依赖Celery 4.1
异步任务基于[Celery模块](http://docs.celeryproject.org/en/latest/)<br />

二、安装
-----------------------------------
```
yum install git
git clone https://github.com/SuperHighMan/celery.git
python3 setup.py install
```

三、开始使用
-----------------------------------
启动后台worker
```
celery -A proj worker -l info -n worker.%h -Q celery
```
四、开发实例
-----------------------------------
```python
from proj.async import AsyncCheck
import datetime

if __name__ == '__main__':
    args = [['192.168.92.133'], 'uptime']
    #自定义设置轮询时间的异步调用
    begin = datetime.datetime.now()
    check = AsyncCheck(args=args, interval=3, times=2)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)

    #使用默认设置的轮询 default: interval=5, times=10
    begin = datetime.datetime.now()
    check = AsyncCheck(args=args)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)
```