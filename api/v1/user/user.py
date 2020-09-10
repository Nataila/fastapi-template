#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28


from fastapi import APIRouter

from extensions import logger
from utils import response_code, tools
from utils.database import db, redis
from werkzeug.security import check_password_hash

from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/login/")
def login(user: User):
    [username, passwd] = map(user.dict().get, ['username', 'password'])
    try:
        db_user = db.user.find_one({'username': username})
        assert db_user
        pwhash = db_user['password']
        passwd_check = check_password_hash(pwhash, passwd)
        assert passwd_check
        token = tools.new_token(20)
        uid = str(db_user['_id'])
        redis.set(token, uid)
        return response_code.resp_200({'token': token, 'username': username, 'id': uid})
    except Exception as e:
        return response_code.resp_401()