#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28


import time
from fastapi import APIRouter

from extensions import logger
from pydantic import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash

from utils import response_code, tools
from utils.database import db, redis
from utils.mailing import send_code

from schemas import user
from core.config import settings
from pymongo import ReturnDocument

router = APIRouter()


@router.post("/read/message/")
def sendmessage(message: user.MessageBase):
    [message_from, message_to, message_content, message_date] = \
            map(message.dict().get, ['message_from', 'message_to', 'message_content', 'message_date'])
    try:
        _id = db.messages.find_one_and_update({
            'message_from': message_from, 
            'message_to': message_to,
            'message_content': message_content}, {'$set':{
            'message_status': True,
            'message_date': message_date
            }},
            retrundocument=ReturnDocument.AFTER)
        assert _id
        logger.info(f'del {message_from} send {message_content} to {message_to} ')
        redis.delete(f'{settings.MESSAGE_KEY}{message_from}:{message_to}', message_content)
        ctx = {'code':'200', 'id': str(_id)}
        return response_code.resp_200(ctx)
    except Exception as e:
        return response_code.resp_500()

# 系统生成message,可以弃用
@router.post("/send/message/")
def sendmessage(message: user.MessageBase):#_from: str, message_to: str, message_content: str):
    [message_from, message_to, message_content, message_status, message_date] = \
            map(message.dict().get, ['message_from', 'message_to', 'message_content', 'message_status', 'message_date'])

    print(message_from, message_to, message_content, message_status, message_date)
    _id = db.messages.insert({
        'message_from': message_from, 
        'message_to': message_to,
        'message_content': message_content,
        'message_status': False,
        'message_date': time.time() 
        })
    logger.info(f'{message_from} send {message_content} to {message_to} ')
    redis.set(f'{settings.MESSAGE_KEY}{message_from}:{message_to}', message_content)
    ctx = {'code':'200', 'id': str(_id)}
    return response_code.resp_200(ctx)

@router.post("/forget/")
def forget(username: str, email: str):
    '''找回密码'''
    [username, email] = map(user.dict().get, ['username', 'email'])
    try:
        db_user = db.user.find_one({'username': username})
        assert db_user
        code = tools.new_token(3)
        send_mail_code(email)
        return response_code.resp_200({'code': code, 'username': username })
    except Exception as e:
        return response_code.resp_401()

@router.post("/newpasswd/")
def newpasswd(email: str, code: str, newpass: str, newpass2:str):
    '''修改密码'''
    if newpass != newpass2:
        return response_code.res_5000('密码不一致')
    flag = email
    redis_code = redis.get(f'{settings.CODE_KEY}{flag}')
    if redis_code != code:
        return response_code.resp_5000('验证码不正确')

    encrypt_passwd = generate_password_hash(newpass)
    db_user = db.user.find_one_and_update({'email': email}, {'$set':{'password': encrypt_passwd}},
            retrundocument=ReturnDocument.AFTER)
    _id = str(db_user['_id'])
    ctx = {'email': email, 'id':_id }
    return response_code.resp_200('修改成功')

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
