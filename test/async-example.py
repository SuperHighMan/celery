#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : kthread.py
# @Author: Hui
# @Date  : 2017/9/20
# @Desc  :

# This is an example file. Maybe you should first install this project first

from proj.async import AsyncCheck
import datetime

if __name__ == '__main__':
    args = [['192.168.92.133'], 'uptime']
    begin = datetime.datetime.now()
    check = AsyncCheck(args=args, interval=3, times=2)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)

    begin = datetime.datetime.now()
    check = AsyncCheck(args=args)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)


