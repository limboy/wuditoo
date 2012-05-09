#coding=utf-8
import time
import logging
from blinker import signal
import formencode
from formencode import validators

import models
from macros.macro import EVENTS

user_create = signal(EVENTS['USER_CREATE'])

class Profile(models.base.BaseThing):
    _invalid_link = {'badURL': u'链接格式不正确',
                   'noTLD': u'链接格式不正确'}

    link_weibo = validators.URL(
            strip = True,
            add_http = True,
            not_empty = False,
            messages = _invalid_link)

    link_qq = validators.URL(
            strip = True,
            add_http = True,
            not_empty = False,
            messages = _invalid_link)

    link_douban = validators.URL(
            strip = True,
            add_http = True,
            not_empty = False,
            messages = _invalid_link)

    link_flickr = validators.URL(
            strip = True,
            add_http = True,
            not_empty = False,
            messages = _invalid_link)

    link_blog = validators.URL(
            strip = True,
            add_http = True,
            not_empty = False,
            messages = _invalid_link)

    @user_create.connect
    def _user_create(user, **kwargs):
        Profile(
            user_id = user.id,
            link_weibo = '',
            link_qq = '',
            link_douban = '',
            link_flickr = '',
            link_blog = '',
        ).save()
