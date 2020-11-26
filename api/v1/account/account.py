#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28


from fastapi import APIRouter, Depends

from extensions import logger
from werkzeug.security import generate_password_hash, check_password_hash

from utils import response_code, tools, depends
from utils.database import db, redis
from utils.mailing import send_code

from schemas import user
from core.config import settings

router = APIRouter()


@router.post("/account/login/", name='登录')
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
    except Exception:
        return response_code.resp_401()


@router.post('/account/send/mail/code/', name="发送验证码")
def send_mail_code(to: str):
    '''发送邮件验证码'''
    code = tools.new_token(3)
    logger.info(f'send {code} to {to}')
    redis.set(f'{settings.CODE_KEY}{to}', code, settings.CODE_KEY_EXPIRE)
    send_code(to, code)
    return response_code.resp_200('ok')


@router.post('/account/signup/', name='注册')
def signup(user: user.UserCreate):
    '''注册'''
    [email, phone, password1] = map(user.dict().get, ['email', 'phone', 'password1'])
    encrypt_passwd = generate_password_hash(password1)
    _id = db.user.insert({'email': email, 'phone': phone, 'password': encrypt_passwd})
    ctx = {'email': email, 'phone': phone, 'id': str(_id)}
    return response_code.resp_200(ctx)


@router.post('/account/changepwd/', name='修改密码')
def changepwd(passwd:user.ChangePwd, user: dict = Depends(depends.token_is_true)):
    '''修改密码'''
    pwhash = user['password']
    old_password = passwd.old_password
    passwd_check = check_password_hash(pwhash, old_password)
    if not passwd_check:
        return response_code.resp_422('密码不正确')
    db.user.find_one_and_update(user, {'$set': {'password': generate_password_hash(passwd.new_password2)}})
    return response_code.resp_200('ok')
