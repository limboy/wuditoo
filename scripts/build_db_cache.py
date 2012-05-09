#!/usr/bin/env python
#coding=utf=8
import config

import json
import tornado.options
from clint.textui import progress
from macros.macro import REDIS_KEY
from utils import get_redis_client
from models import Photo, User

def run():
    redis_client = get_redis_client()
    for table in ('photo', 'user'):
        redis_key = REDIS_KEY['TABLE_ITEMS'].format(table = table)
        if table == 'photo':
            result = Photo().findall_by_status(0, limit = 1000000)
        elif table == 'user':
            result = User().findall(limit = 1000000)

        for item in progress.bar(result):
            redis_client.hset(redis_key, item.id, json.dumps(item.to_dict()))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    run()

