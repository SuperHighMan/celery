#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from proj.celery import app
import time
import os

@app.task
def taskA(x, y):
    time.sleep(30)
    return x + y

@app.task
def taskB(x, y, z):
    time.sleep(5)
    return x * y + z

@app.task
def power(x):
    time.sleep(2)
    return x * x

@app.task
def ssh_command(ip, cmd):
    c = "ssh " + ip + " " + cmd
    out = os.popen(c)
    return out.readlines()
