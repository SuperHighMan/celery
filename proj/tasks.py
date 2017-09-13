#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from proj.celery import app
import time

@app.task
def taskA(x, y):
    time.sleep(10)
    return x + y

@app.task
def taskB(x, y, z):
    time.sleep(5)
    return x * y + z

@app.task
def power(x):
    time.sleep(3)
    return x * x
