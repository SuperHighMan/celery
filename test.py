#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import datetime
import time

from celery.exceptions import TimeoutError

from proj.async import AsyncCheck
from proj.easy.tasks import power
from proj.util.common import timeout
from proj.complex.tasks import test1

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

def async_class_test():
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

@timeout(5)
def method_timeout(seconds, text):
    print('start', seconds, text)
    time.sleep(seconds)
    print('finish', seconds, text)
    return seconds


def time_test():
    begin = datetime.datetime.now()
    for i in range(0,10):
        r = test1.delay(i,i)
        Result_ID.append(r)

    while(1):
        for j in Result_ID:
            if j.status == "SUCCESS":
                print(j.get())
                Result_ID.remove(j)
            elif j.status == 'FAILURE':
                Result_ID.remove(j)
            else:
                pass
        if len(Result_ID) == 0:
            break

    end = datetime.datetime.now()
    print(end - begin)


if __name__ == '__main__':
    # Return AsyncResult
    #async_fun()
    #print
    '''
    begin = datetime.datetime.now()
    for sec in range(1, 30):
        try:
            print('*' * 20)
            print(method_timeout(sec, 'test waiting %d seconds' % sec))
        except Timeout as e:
            print(e)
    end = datetime.datetime.now()
    print(end - begin)
    '''

    time_test()




