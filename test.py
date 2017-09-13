#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from proj.tasks import taskA, taskB, power
import time
import datetime

from celery.exceptions import TimeoutError

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
    '''
    r = add.delay(100, 10)

    print(r.status)
    print(r.id)
    print(r.get(timeout=15))
    '''
    #async_fun()
    t1 = taskA.delay(2, 3)
    print(t1)
    time.sleep(20)
    print(t1.status)



