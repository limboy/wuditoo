#coding=utf-8
import logging
import time
import models
from blinker import signal
from macros.macro import EVENTS

class Photo_Comment(models.base.BaseThing):
    @property
    def creator(self):
        return models.user.User().find(self.user_id)

    def delete(self):
        self.status = -1
        self.save()
        signal(EVENTS['PHOTO_COMMENT_DELETE']).send(self)

    def create(self):
        self.updated = self.created = time.time()
        self.status = 0
        self.save()
        signal(EVENTS['PHOTO_COMMENT_ADD']).send(self)
