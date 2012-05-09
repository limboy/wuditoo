#coding=utf-8
import time
from blinker import signal

from macros.macro import EVENTS
import models

photo_delete = signal(EVENTS['PHOTO_DELETE'])

class Photo_Like(models.base.BaseThing):
    def like(self, user_id, photo_id):
        liked = self.where('user_id', '=', user_id)\
                    .where('photo_id', '=', photo_id)\
                    .find()
        if not liked:
            self.reset()
            self.user_id = user_id
            self.photo_id = photo_id
            self.save()
            signal(EVENTS['PHOTO_LIKE']).send(self)
            return self.saved
        return False

    def unlike(self, user_id, photo_id):
        liked = self.where('user_id', '=', user_id)\
                    .where('photo_id', '=', photo_id)\
                    .find()
        if liked:
            signal(EVENTS['PHOTO_UNLIKE']).send(self)
            self.reset()
            rowcount = self.where('user_id', '=', user_id)\
                .where('photo_id', '=', photo_id)\
                .delete()
            return rowcount
        return False

    @photo_delete.connect
    def _photo_delete(photo):
        Photo_Like().where('photo_id', '=', photo.id).delete()
