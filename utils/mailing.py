#!/usr/bin/env python
# coding: utf-8
# cc@2020/09/11

import logging

from redis import Redis

from rq.decorators import job

from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

from core.config import settings


@job('default', connection=Redis(), timeout=settings.EMAILS_TIMEOUT)
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
    if settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_code(email_to: str, code: str) -> None:
    subject = f"fastapi验证码"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "code.html") as f:
        template_str = f.read()
    send_email.delay(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"code": code, "email": email_to},
    )
