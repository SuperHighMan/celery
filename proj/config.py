#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from kombu import Exchange,Queue

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/1'

CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("for_task_A", Exchange("for_task_A"), routing_key="task_a"),
    Queue("for_task_B", Exchange("for_task_B"), routing_key="task_b")
)

CELERY_ROUTES = {
    'proj.tasks.taskA':{"queue":"for_task_A", "routing_key":"task_a"},
    'proj.tasks.taskB':{"queue":"for_task_B", "routing_key":"task_b"}
}


