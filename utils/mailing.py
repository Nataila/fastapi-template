#!/usr/bin/env python
# coding: utf-8
# cc@2020/09/11

from redis import Redis

from rq.decorators import job

from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

from config import settings

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")



# @job('default', connection=Redis(), timeout=EMAIL_CONF['EMAIL_TIMEOUT'])
# def send(to, header, content):
#     # 1. 连接邮箱服务器
#     con = smtplib.SMTP_SSL(EMAIL_CONF['HOST'], EMAIL_CONF['PORT'])
#     # 2. 登录邮箱
#     con.login(EMAIL_CONF['HOST_USER'], EMAIL_CONF['HOST_PASSWORD'])
#     # 2. 准备数据
#     # 创建邮件对象
#     msg = MIMEMultipart()
#     # 设置邮件主题
#     subject = Header(header, 'utf-8').encode()
#     msg['Subject'] = subject
#     # 设置邮件发送者
#     msg['From'] = EMAIL_CONF['DEFAULT_FROM_EMAIL']
#     # 设置邮件接受者
#     msg['To'] = to
#     msg.attach(content)
#     # 3.发送邮件
#     con.sendmail(EMAIL_CONF['HOST_USER'], to, msg.as_string())
#     con.quit()
# 
# 
# def send_code(code, to):
#     with open('./templates/code.html', 'r+', encoding='utf-8') as f:
#         html = f.read()
#         html = html.format(**{'code': code})
#         html = MIMEText(html, 'html', 'utf-8')
#         send(to, '验证码', html)
