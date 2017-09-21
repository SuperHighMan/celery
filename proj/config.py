#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from kombu import Exchange,Queue
from celery.schedules import crontab
from datetime import timedelta

# 结果存放 Backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Broker设置
BROKER_URL = 'redis://127.0.0.1:6379/1'
#时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("for_task_A", Exchange("for_task_A"), routing_key="task_a"),
    Queue("for_task_B", Exchange("for_task_B"), routing_key="task_b")
)

CELERY_ROUTES = {
    'proj.easy.tasks.taskA':{"queue":"for_task_A", "routing_key":"task_a"},
    'proj.easy.tasks.taskB':{"queue":"for_task_B", "routing_key":"task_b"}
}

# 计划任务配置
CELERYBEAT_SCHEDULE = {
    # 每分钟执行一次taskA任务
    'taskA-every-minute': {
        'task': 'proj.easy.tasks.taskA',
        'schedule': crontab(minute='*/1'),
        #'schedule': timedelta(seconds=60),
        'args': (3, 19)
    }
}

