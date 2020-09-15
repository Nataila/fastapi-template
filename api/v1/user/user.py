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


@router.post("/forget/")
def forget(username: str, email: str):
    '''找回密码'''
    [username, email] = map(user.dict().get, ['username', 'email'])
    try:
        db_user = db.user.find_one({'username': username})
        assert db_user
        code = tools.new_token(3)
        send_mail_code(email)
        return response_code.resp_200({'token': token, 'username': username })
    except Exception as e:
        return response_code.resp_401()

@router.post("/newpasswd/")
def newpasswd(email: str, code: str, newpass: str):
    '''修改密码'''
    flag = 'email'
    redis_code = redis.get(f'{settings.CODE_KEY}{flag}')
    if redis_code != code:
        return response_code.resp_401()

    encrypt_passwd = generate_password_hash(newpass)
    db_user = db.user.find_one_and_update({'email': email},{'$set':{'password': encrypt_passwd}})
    _id = str(db_user['_id'])
    ctx = {'email': email,'id':_id }
    return response_code.resp_200(ctx)

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
