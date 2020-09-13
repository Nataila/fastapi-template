#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 14:47
# @Author  : CoderCharm
# @File    : development_config.py
# @Software: PyCharm
# @Desc    :
"""

开发环境配置

"""
from .settings import Settings as mainSettings


class Settings(mainSettings):
    # Mongodb配置
    MONGODB = {
        'host': '127.0.0.1',
        'port': 27017,
    }

    # redis配置
    REDIS = {
        'host': '127.0.0.1',
        'port': 6379,
        'db': '5',
        'password': '',
        'decode_responses': True,
    }

    EMAIL_CONF = {
        # 发邮件配置
        'HOST': 'smtp.163.com',
        'PORT': 465,
        'HOST_USER': 'xxx@163.com',
        'HOST_PASSWORD': '******',
        'EMAIL_TIMEOUT': 120,
        'DEFAULT_FROM_EMAIL': 'xxx@163.com <xxx@163.com>',
    }


settings = Settings()
