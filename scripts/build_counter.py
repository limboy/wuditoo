#!/usr/bin/env python
#coding=utf=8
import config

import tornado.options
from clint.textui import progress
from macros.macro import REDIS_KEY
from utils import get_redis_client
from models import Photo, Photo_Like

def run():
    redis_client = get_redis_client()
    redis_client.delete(REDIS_KEY['USER_LIKED_COUNT'])
    redis_client.delete(REDIS_KEY['USER_LIKES_COUNT'])
    redis_client.delete(REDIS_KEY['USER_PHOTO_COUNT'])
    photos = Photo().select(['id', 'user_id', 'likes_count']).where('status', '=', 0).findall(limit=1000000)
    for photo in progress.bar(photos):
        current_liked_count = redis_client.hget(REDIS_KEY['USER_LIKED_COUNT'], photo.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_LIKED_COUNT'], photo.user_id, int(current_liked_count) + int(photo.likes_count))

        current_photo_count = redis_client.hget(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id) or 0
        redis_client.hset(REDIS_KEY['USER_PHOTO_COUNT'], photo.user_id, int(current_photo_count) + 1)

        photo_like = Photo_Like().findall_by_photo_id(photo.id)
        for item in photo_like:
            current_likes_count = redis_client.hget(REDIS_KEY['USER_LIKES_COUNT'], item.user_id) or 0
            redis_client.hset(REDIS_KEY['USER_LIKES_COUNT'], item.user_id, int(current_likes_count) + 1)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    run()
