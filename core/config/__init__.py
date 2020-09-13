#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:37
# @Author  : cc

"""
配置文件
local_settings 配置本地敏感配置，比如私钥、密码等
防止提交到版本库
"""

try:
    from .local_settings import settings

    print("----------已启动------------")
except ModuleNotFoundError:
    print('-------------------------------')
    print('please cp local_settings_example.py local_settings.py and setting it!!!')
    print('-------------------------------')
    from .settings import settings
