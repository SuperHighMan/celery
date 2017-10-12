#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : findip.py
# @Author: Hui
# @Date  : 2017/10/12
# @Desc  : python正则表达式练习，用于匹配ip

import re

def findip(file, path):
    pattern = '[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}'
    result = open(path, 'w+')
    with open(file) as f:
        for line in f:
            list = re.findall(pattern, line)
            for i in list:
                result.write(i)
                result.write('\n')
    result.close()


if __name__ == '__main__':
    findip('/var/log/messages', 'tmp')
    print('hello')