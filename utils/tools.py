#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/25

import binascii
import os


def new_token(length=8):
    """
    生成随机字串
    """
    return binascii.hexlify(os.urandom(length)).decode()
