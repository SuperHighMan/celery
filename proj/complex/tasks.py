#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: Hui
# @Date  : 2017/9/21
# @Desc  :

from __future__ import absolute_import
from proj.celery import app
from proj.util.common import timeout
import time
import os

@app.task
@timeout(2)
def test1(x, y):
    time.sleep(30)
    return x + y