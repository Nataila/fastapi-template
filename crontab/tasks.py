#!/usr/bin/env python
# coding: utf-8
# cc@2020/11/27

import time
from apscheduler.schedulers.blocking import BlockingScheduler


def every1m():
    '''每一分钟运行的任务'''
    pass

scheduler = BlockingScheduler()

# 每隔 1分钟 运行
scheduler.add_job(every1m, 'interval', minutes=1)

scheduler.start()
