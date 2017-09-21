#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('proj', include=['proj.easy.tasks', 'proj.complex.tasks'])

app.config_from_object('proj.config')

if __name__ == '__main__':
    app.start()
