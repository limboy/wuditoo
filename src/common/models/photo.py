#coding=utf-8
import time
import datetime
import logging
from blinker import signal
from formencode import validators

from macros.macro import EVENTS, REDIS_KEY
import models
from utils import get_redis_client, calculate_photo_karma, process_photo_url

photo_like = signal(EVENTS['PHOTO_LIKE'])
photo_unlike = signal(EVENTS['PHOTO_UNLIKE'])
photo_delete = signal(EVENTS['PHOTO_DELETE'])
photo_comment_delete = signal(EVENTS['PHOTO_COMMENT_DELETE'])
photo_comment_add = signal(EVENTS['PHOTO_COMMENT_ADD'])
photo_after_validation = signal('photo.after_validation')

class Photo(models.base.BaseThing):
    _photo_soure_error = {'empty': u'照片地址不能为空', 'badURL': u'链接格式不正确', 'noTLD': u'链接格式不正确'}
    _page_soure_error = {'empty': u'页面址不能为空', 'badURL': u'链接格式不正确', 'noTLD': u'链接格式不正确'}

    title = validators.String(
            not_empty = True,
            strip = True,
            messages = {
                'empty': u'别忘了填写标题哦',
                }
            )

    photo_source = validators.URL(
            strip = True,
            add_http = True,
            not_empty = True,
            messages = _photo_soure_error)

    page_source = validators.URL(
            strip = True,
            add_http = True,
            not_empty = True,
            messages = _page_soure_error)

    @property
    def comments(self):
        return models.Photo_Comment().findall_by_photo_id_and_status(self.id, 0)

    def create(self):
        self.status = 0
        self.created = self.updated = time.time()
        self.karma = calculate_photo_karma(0, self.created)
        self.save()
        if self.saved:
            signal(EVENTS['PHOTO_CREATE']).send(self)
            return self.id

    def delete(self):
        self.status = -1
        self.save()
        signal(EVENTS['PHOTO_DELETE']).send(self)

    def get_hot(self, limit, offset):
        return Photo().order_by('-karma').findall_by_status(0, limit = limit, offset = offset)

    def get_hot_count(self):
        return Photo().count_by_status(0)

    @property
    def creator(self):
        return models.User().find(self.user_id)

    @photo_after_validation.connect
    def _photo_after_validation(photo):
        if not photo.id:
            hashval = process_photo_url(photo.photo_source, photo.user_id)
            if not hashval:
                photo.add_error(photo_source = u'此链接无法被抓取')
            else:
                photo.hash = hashval

    @photo_like.connect
    def _photo_like(photo_like):
        photo = Photo().find(photo_like.photo_id)
        photo.likes_count += 1
        photo.karma = calculate_photo_karma(photo.likes_count, photo.created)
        photo.save()

    @photo_unlike.connect
    def _photo_unlike(photo_like):
        photo = Photo().find(photo_like.photo_id)
        photo.likes_count -= 1
        photo.karma = calculate_photo_karma(photo.likes_count, photo.created)
        photo.save()

    @photo_comment_delete.connect
    def _photo_comment_delete(comment):
        photo = Photo().find(comment.photo_id)
        photo.comments_count -= 1
        photo.save()

    @photo_comment_add.connect
    def _photo_comment_add(comment):
        photo = Photo().find(comment.photo_id)
        photo.comments_count += 1
        photo.save()

