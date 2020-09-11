#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28

from core.config import settings
from redis import Redis
from pymongo import MongoClient

client = MongoClient(**settings.MONGODB)
db = client['pyq']

redis = Redis(**settings.REDIS)
