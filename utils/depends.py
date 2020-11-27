#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/25

from bson import ObjectId

from fastapi import Header, HTTPException, Depends

from .database import db, redis

from .response_code import resp_401


async def token_is_true(token: str = Header(..., description="token验证")):
    uid = redis.get(token)
    if not uid:
        raise HTTPException(
            status_code=401, detail="Authentication failed",
        )
    user = db.user.find_one({'_id': ObjectId(uid)})
    return user


async def is_superuser(user: dict = Depends(token_is_true)):
    if not user.group == 1:
        raise HTTPException(
            status_code=403, detail="Authentication failed",
        )
    return user
