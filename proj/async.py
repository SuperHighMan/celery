#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import time
from datetime import datetime, timedelta

from proj.easy.tasks import ssh_command, taskA


class AsyncCheck:
    # args [["10.10.10.10", "10.10.10.11"],
    #       "uptime"]
    def __init__(self, args, **kwargs):
        self.__iplist = args[0]
        self.__str = args[1]
        if 'times' in kwargs.keys():
            self.__times = kwargs['times']
        else:
            self.__times = 10
        if 'interval' in kwargs.keys():
            self.__interval = kwargs['interval']
        else:
            self.__interval = 5
        self.__result = []

    def timeout_result(self):
        return self.__result

    def run(self):
        for ip in self.__iplist:
            ip = ip.rstrip()
            task = ssh_command.apply_async(args = [ip, self.__str] )
            self.__result.append(task)

        for times in range(0, self.__times):
            time.sleep(self.__interval)
            for tmp in self.__result:
                if tmp.status == 'SUCCESS':
                    self.__result.remove(tmp)
                    print(tmp.get())
            if len(self.__result) == 0:
                break

    def run_by_queue(self):
            #task = ssh_command.apply_async(args = [ip, self.__str] )
        task = taskA.apply_async(args = [4, 8], queue='celery', expires=datetime.utcnow()+timedelta(seconds=1) )
        self.__result.append(task)

        for times in range(0, self.__times):
            time.sleep(self.__interval)
            for tmp in self.__result:
                if tmp.status == 'SUCCESS':
                    self.__result.remove(tmp)
                    print(tmp.get())
            if len(self.__result) == 0:
                break