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
from typing import Union, Optional
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress
from .config import Config as productionConfig


class Config(productionConfig):
    # 文档地址
    DOCS_URL: str = "/api/v1/docs"
    # # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/v1/openapi.json"
    # 禁用 redoc 文档
    REDOC_URL: Optional[str] = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = ''

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
        'HOST_USER': '',
        'HOST_PASSWORD': '',
        'EMAIL_TIMEOUT': 120,
        'DEFAULT_FROM_EMAIL': 'xx@163.com <xx@163.com>'
    }




config = Config()
