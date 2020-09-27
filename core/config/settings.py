#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 10:15

import os

from typing import Union, Optional
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress, EmailStr


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    # 文档地址 成产环境可以关闭 None
    DOCS_URL: Optional[str] = "/api/v1/docs"
    # # 文档关联请求数据接口 成产环境可以关闭 None
    OPENAPI_URL: Optional[str] = "/api/v1/openapi.json"
    # 禁用 redoc 文档
    REDOC_URL: Optional[str] = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 天
    SECRET_KEY: str = '-*&^)()sd(*A%&^aWEQaasda_asdasd*&*)(asd%$#'

    # 发送邮件配置
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_TEMPLATES_DIR = os.path.join(BASE_DIR, 'utils/templates/email')
    EMAILS_ENABLED: bool = True
    EMAILS_TIMEOUT: int = 60

    CODE_KEY = 'code:'
    # 验证码失效时间 10分钟
    CODE_KEY_EXPIRE = 60 * 10

    # Mongodb配置
    MONGODB = {
        'host': '127.0.0.1',
        'port': 27017,
    }

    MONGODB_DB = 'fastapi'

    # redis配置
    REDIS = {
        'host': '127.0.0.1',
        'port': 6379,
        'db': '5',
        'password': '',
        'decode_responses': True,
    }


settings = Settings()
