#coding=utf-8
import thing
import time
import datetime
import logging
import formencode
from formencode import validators
from blinker import signal

from utils import (hash_password,
                   get_redis_client,
                   cached_property,
                   calculate_user_level)
import models
from macros.macro import (PASSWORD_SALT,
                          EVENTS,
                          REDIS_KEY,
                          USER_LEVEL_CN,
                          USER_LEVEL_PHOTOS_PER_WEEK)

photo_like = signal(EVENTS['PHOTO_LIKE'])
photo_delete = signal(EVENTS['PHOTO_DELETE'])
photo_unlike = signal(EVENTS['PHOTO_UNLIKE'])
photo_create = signal(EVENTS['PHOTO_CREATE'])

class User(models.base.BaseThing):
    email = validators.Email(
            not_empty = True,
            strip = True,
            messages = {'noAt': u'这可不是一个正常的邮箱哦',
                        'empty': u'忘了填邮箱啦'})

    username = formencode.All(
            validators.String(
                 not_empty = True,
                 strip = True,
                 min = 4,
                 max = 24,
                 messages = {
                     'empty': u'用户名总得有一个吧',
                     'tooLong': u'这么长的用户名没有必要吧',
                     'tooShort': u'用户名长度不能少于4'}),
             validators.PlainText(messages = {
                     'invalid': u'用户名只能包含数字，字母和下划线'
                  }))

    fullname = validators.String(
                 not_empty = True,
                 strip = True,
                 max = 12,
                 messages = {
                     'empty': u'总得有个昵称吧',
                     'tooLong': u'这么长的昵称没有必要吧',
                     }
                 )

    password = validators.String(not_empty = True,
                                 messages = {'empty': u'忘记设置密码了'})

    def create(self):
        self.fullname = self.username
        self.created = time.time()

        if self.validate():
            if User().find_by_username(self.username):
                self.errors = {'username': u'此用户名已被占用'}
                return
            if User().find_by_email(self.email):
                self.errors = {'email': u'此Email已被注册'}
                return
            if not self.password_confirm:
                self.errors = {'password_confirm': u'确认密码不能为空'}
                return
            if self.password != self.password_confirm:
                self.errors = {'password': u'两次密码输入不一致'}
                return

            invite_key = models.Invite_Key().find_by_hash(self.invite_key)
            if not invite_key:
                self.errors = {'invite_key': u'该邀请码不存在'}
                return
            if invite_key.used:
                self.errors = {'invite_key': u'该邀请码已被使用'}
                return

            del self.password_confirm
            del self.invite_key
            self.password = hash_password(self.password)
            user_id = self.save()
            signal(EVENTS['USER_CREATE']).send(self, invite_key_hash = invite_key.hash)
            return user_id

    def change_password(self, origin_password, password, password_confirm):
        if not origin_password:
            self.add_error(origin_password = u'当前密码不能为空')
        if not password:
            self.add_error(password = u'新密码不能为空')
        if not password_confirm:
            self.add_error(password_confirm = u'确认密码不能为空')
        
        if password != password_confirm:
            self.add_error(password_confirm = u'两次密码输入不一致')

        if self.errors:
            return False

        if hash_password(origin_password) != self.password:
            self.add_error(origin_password = u'当前密码不正确')
            return False

        self.password = hash_password(password)
        self.save()
        return self.saved

    def is_following(self, dest_user_id):
        return models.FollowShip().count_by_follower_user_id_and_followed_user_id(self.id, dest_user_id)

    def has_liked_photo(self, photo):
        return models.Photo_Like().count_by_user_id_and_photo_id(self.id, photo.id)

    @property
    def is_admin(self):
        return self.id == 1

    @property
    def photo_count(self):
        return get_redis_client().hget(REDIS_KEY['USER_PHOTO_COUNT'], self.id) or 0

    @property
    def liked_count(self):
        return get_redis_client().hget(REDIS_KEY['USER_LIKED_COUNT'], self.id) or 0

    @property
    def likes_count(self):
        return get_redis_client().hget(REDIS_KEY['USER_LIKES_COUNT'], self.id) or 0

    @property
    def following_count(self):
        return models.FollowShip().count_by_follower_user_id(self.id)

    @property
    def follower_count(self):
        return models.FollowShip().count_by_followed_user_id(self.id)

    @property
    def unused_invite_key_count(self):
        return models.Invite_Key().count_by_user_id_and_used(self.id, 0)

    @property
    def profile(self):
        if not getattr(self, '_profile'):
            profile = models.Profile().find_by_user_id(self.id)
            self._profile = profile
        return self._profile

    @property
    def left_upload_count(self):
        if self.is_admin:
            return 100
        init_count = USER_LEVEL_PHOTOS_PER_WEEK[self.level]
        now = datetime.datetime.now()
        dt = now - datetime.timedelta(days = datetime.datetime.weekday(now))
        start_week_timestamp = time.mktime(datetime.datetime.date(dt).timetuple())
        created_count = models.Photo().where('created', '>', start_week_timestamp)\
               .where('status', '=', 0)\
               .where('user_id', '=', self.id)\
               .count()
        return init_count - created_count

    @photo_like.connect
    def _photo_like(photo_like):
        """
        re calculate user level here
        """
        user = models.User().find(models.Photo().find(photo_like.photo_id).user_id)

        redis_client = get_redis_client()
        redis_client.hincrby(REDIS_KEY['USER_LIKED_COUNT'], user.id, 1)

        current_likes_count = redis_client.hget(REDIS_KEY['USER_LIKES_COUNT'], photo_like.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_LIKES_COUNT'], photo_like.user_id, int(current_likes_count) + 1)

        calculated_user_level = calculate_user_level(user)
        if calculated_user_level > user.level:
            redis_key = REDIS_KEY['USER_MESSAGE'].format(user_id = user.id)
            models.Invite_Key().gen_by_level(user, calculated_user_level, user.level)
            msg = u"{0}|恭喜你，成功升级到{1}".format('info', USER_LEVEL_CN[calculated_user_level])
            redis_client.lpush(redis_key, msg)
            user.level = calculated_user_level
            user.save()

    @photo_unlike.connect
    def _photo_unlike(photo_like):
        """
        re calculate user level here
        """
        user = models.User().find(models.Photo().find(photo_like.photo_id).user_id)

        redis_client = get_redis_client()
        redis_client.hincrby(REDIS_KEY['USER_LIKED_COUNT'], user.id, -1)

        current_likes_count = redis_client.hget(REDIS_KEY['USER_LIKES_COUNT'], photo_like.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_LIKES_COUNT'], photo_like.user_id, int(current_likes_count) - 1)

    @photo_create.connect
    def _photo_create(photo):
        redis_client = get_redis_client()
        current_photo_count = redis_client.hget(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id, int(current_photo_count) + 1)

    @photo_delete.connect
    def _photo_delete(photo):
        redis_client = get_redis_client()
        current_photo_count = redis_client.hget(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id, int(current_photo_count) - 1)
