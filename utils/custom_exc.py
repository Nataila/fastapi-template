#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/21 11:13
# @Author  : CoderCharm
# @File    : custom_exc.py
# @Software: PyCharm
# @Desc    :

"""
自定义异常
"""

from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from pydantic import ValidationError


class PostParamsError(Exception):
    def __init__(self, err_desc: str = "POST请求参数错误"):
        self.err_desc = err_desc


class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "token认证失败"):
        self.err_desc = err_desc


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
