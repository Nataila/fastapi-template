#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:48
# @Author  : CoderCharm
# @File    : home.py
# @Software: PyCharm
# @Desc    :
"""

"""

from fastapi import Depends, APIRouter, Query

from extensions import logger
from utils import response_code

router = APIRouter()


@router.get("/home")
def home_banner():
    return response_code.resp_200('ok')
