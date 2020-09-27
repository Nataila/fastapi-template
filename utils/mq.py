 #!/usr/bin/env python
 # coding: utf-8

import logging 

from redis import Redis
from .database import db

from rq.decorators import job

from pathlib import Path
from typing import Any, Dict, Optional

from core.config import settings

import time

@job('default', connection=Redis())
def send_message(
    message_from: str, # service name
    message_to: str, #user id
    message_content: str,
    message_status: bool,
         ) -> None:
    db.messages.insert({'message_from': message_from, 'message_to': message_to,
        'message_content': message_content,
        'message_status': False,
        'message_date': time.time()
        })

    logger.info(f'del {message_from} send {message_content} to {message_to} ')
