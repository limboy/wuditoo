#coding=utf-8
import logging
import models
from utils import get_redis_client
from macros.macro import REDIS_KEY, EVENTS
from blinker import signal

photo_delete = signal(EVENTS['PHOTO_DELETE'])

class Photo_Tag(models.base.BaseThing):
    @property
    def hot_tags(self):
        redis_key = REDIS_KEY['HOT_TAGS']
        redis_client = get_redis_client()
        if not redis_client.scard(redis_key):
            hot_tags = self.query(
                    '''
                    SELECT tag, count(id) 
                    FROM photo_tag 
                    GROUP BY tag 
                    ORDER BY count(id) DESC
                    LIMIT 100
                    '''
                    ).fetchall()
            for item in hot_tags:
                redis_client.sadd(redis_key, item.tag)
            # expires 1 hour later
            redis_client.expire(redis_key, 3600)
        
        tags = []
        if redis_client.smembers(redis_key):
            length = min(10, redis_client.scard(redis_key))
            for i in range(length):
                tag = redis_client.spop(redis_key)
                tags.append(tag)
            for i in range(length):
                redis_client.sadd(redis_key, tags[i])
        return tags

    @photo_delete.connect
    def _photo_delete(photo):
        Photo_Tag().where('photo_id', '=', photo.id).delete()
