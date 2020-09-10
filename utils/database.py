#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28

from settings import config
from redis import Redis
from pymongo import MongoClient

client = MongoClient(**config.MONGODB)
db = client['pyq']

redis = Redis(**config.REDIS)
