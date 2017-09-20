#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from proj.tasks import taskA, taskB, power
import time
import datetime

from celery.exceptions import TimeoutError
from proj.async import AsyncCheck
Result_ID = []

def async_fun():
    begin = datetime.datetime.now()
    for i in range(1,30):
        r = power.delay(i)
        Result_ID.append(r)

    #time.sleep(1)
    for i in Result_ID:
        try:
            print(i.get(timeout=3))
        except TimeoutError as e:
            print(i.id)
            print(e)
    end = datetime.datetime.now()
    print(end - begin)

if __name__ == '__main__':
    # Return AsyncResult
    #async_fun()
    #print

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

    begin = datetime.datetime.now()
    check = AsyncCheck(args=args)
    check.run_by_queue()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)



