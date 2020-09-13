import re

from typing import Optional

from pydantic import BaseModel, EmailStr, validator

from utils.database import db, redis
from core.config import settings


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    phone: str = None
    code: str
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('两次密码不一致')
        return v

    @validator('email')
    def email_is_exists(cls, email):
        if not email:
            return email
        is_exists = db.user.find({'email': email}).count()
        if is_exists:
            raise ValueError('该用户已存在')
        return email

    @validator('phone')
    def email_or_phone_exists(cls, phone, values, **kwargs):
        email = values.get('email')
        is_exists = db.user.find({'phone': phone}).count()
        if is_exists:
            raise ValueError('该用户已存在')
        if email and phone:
            raise ValueError('邮箱和手机只能选一')
        if phone:
            reg = "1[3|4|5|7|8][0-9]{9}"
            if not re.findall(reg, phone):
                raise ValueError('手机号格式不正确')
        return v

    @validator('code')
    def valid_code(cls, code, values):
        [email, phone] = map(values.get, ['email', 'phone'])
        flag = email or phone
        redis_code = redis.get(f'{settings.CODE_KEY}{flag}')
        if redis_code != code:
            raise ValueError('验证码不正确')
        return code


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
