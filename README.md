A First celery project
===================================
结合celery开发的一个关于celery的小程序，可用于异步任务的调度。

一、环境要求
-----------------------------------
本程序基于Python3开发，推荐>=Python3.5，依赖Celery  4.1
异步任务基于[Celery模块](http://docs.celeryproject.org/en/latest/)<br />
消息中间键使用了redis，推荐使用epel的源进行安装
```
pip3 install celery -i https://pypi.douban.com/simple #推荐使用豆瓣的镜像
yum install redis
```
epel阿里云源
```
[epel]
name=Extra Packages for Enterprise Linux 6 - $basearch
baseurl=http://mirrors.aliyun.com/epel/6/$basearch
        http://mirrors.aliyuncs.com/epel/6/$basearch
#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
 
[epel-debuginfo]
name=Extra Packages for Enterprise Linux 6 - $basearch - Debug
baseurl=http://mirrors.aliyun.com/epel/6/$basearch/debug
        http://mirrors.aliyuncs.com/epel/6/$basearch/debug
#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-debug-6&arch=$basearch
failovermethod=priority
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
gpgcheck=0
 
[epel-source]
name=Extra Packages for Enterprise Linux 6 - $basearch - Source
baseurl=http://mirrors.aliyun.com/epel/6/SRPMS
        http://mirrors.aliyuncs.com/epel/6/SRPMS
#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-source-6&arch=$basearch
failovermethod=priority
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
gpgcheck=0
```

二、安装
-----------------------------------
```
yum install git
git clone https://github.com/SuperHighMan/celery.git
cd celery
python3 setup.py install
```

三、开始使用
-----------------------------------
1.redis启动
```
#远程连接需要配置/etc/redis.conf文件
#bind 127.0.0.1
protected-mode no
此配置仅使用于测试，存在安全风险

#启动redis服务
service redis start

#客户端调用
$redis-cli
127.0.0.1:6379> 
```

2.celery启动后台worker
```
前台启动
ln -s /usr/local/python3/bin/celery /usr/bin/celery
celery -A proj worker -l info -n worker.%h -Q celery

后台启动
celery multi start 1 -A proj -l info -c4 -Q celery --pidfile=/var/run/celery/%n.pid
celery multi stop 1 -A proj -l info -c4 -Q celery --pidfile=/var/run/celery/%n.pid
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