#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : common.py
# @Author: Hui
# @Date  : 2017/9/20
# @Desc  :

import datetime

from proj.util.kthread import KThread


class Timeout(Exception):
    """function run timeout"""


def timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):
        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
            else:
                return result[0]

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator

import time

@timeout(5)
def method_timeout(seconds, text):
    print('start', seconds, text)
    time.sleep(seconds)
    print('finish', seconds, text)
    return seconds

if __name__ == '__main__':
    begin = datetime.datetime.now()
    for sec in range(1, 30):
        #try:
        print('*' * 20)
        print(method_timeout(sec, 'test waiting %d seconds' % sec))
        #except Timeout as e:
        #    print('time out')
    end = datetime.datetime.now()
    print(end - begin)