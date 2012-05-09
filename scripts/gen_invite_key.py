#!/usr/bin/env python
#coding=utf=8
import config

import tornado.options
import models
from utils import gen_invite_key

def run():
    hash = gen_invite_key()
    models.Invite_Key(
            user_id = 0,
            hash = hash,
            ).save()
    print '/register?invite_key=%s'%hash

if __name__ == '__main__':
    tornado.options.parse_command_line()
    run()

