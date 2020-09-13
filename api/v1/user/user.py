#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28


from fastapi import APIRouter

from extensions import logger
from pydantic import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash

from utils import response_code, tools
from utils.database import db, redis
from utils.mailing import send_code

from schemas import user
from core.config import settings

router = APIRouter()


@router.post("/login/")
def login(user: user.UserSignin):
    '''登录'''
    [email, phone] = map(user.dict().get, ['email', 'phone'])
    user = db.user.find_one({'$or': [{'email': email}, {'phone': phone}]})
    try:
        token = tools.new_token(20)
        uid = str(user['_id'])
        redis.set(token, uid)
        return response_code.resp_200(
            {'token': token, 'email': email, 'phone': phone, 'id': uid}
        )
    except Exception as e:
        return response_code.resp_401()


@router.post('/send/mail/code/')
def send_mail_code(to: str):
    '''发送邮件验证码'''
    code = tools.new_token(3)
    logger.info(f'send {code} to {to}')
    redis.set(f'{settings.CODE_KEY}{to}', code, settings.CODE_KEY_EXPIRE)
    send_code(to, code)
    return response_code.resp_200('ok')


@router.post('/signup/')
def signup(user: user.UserCreate):
    '''注册'''
    [email, phone, password1] = map(user.dict().get, ['email', 'phone', 'password1'])
    encrypt_passwd = generate_password_hash(password1)
    _id = db.user.insert({'email': email, 'phone': phone, 'password': encrypt_passwd})
    ctx = {'email': email, 'phone': phone, 'id': str(_id)}
    return response_code.resp_200(ctx)
