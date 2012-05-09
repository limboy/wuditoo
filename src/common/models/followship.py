#coding=utf-8
import logging
from blinker import signal

from macros.macro import EVENTS
import models

class FollowShip(models.base.BaseThing):
    def follow(self, user_id, dest_user_id):
        if not self.count_by_follower_user_id_and_followed_user_id(user_id, dest_user_id):
            self.follower_user_id = user_id
            self.followed_user_id = dest_user_id
            self.save()
            signal(EVENTS['USER_FOLLOW']).send(self)
            return self.saved
        return False

    def unfollow(self, user_id, dest_user_id):
        if self.count_by_follower_user_id_and_followed_user_id(user_id, dest_user_id):
            result = self.where('follower_user_id', '=', user_id)\
                         .where('followed_user_id', '=', dest_user_id)\
                         .find()
            delete = result.delete()
            signal(EVENTS['USER_UNFOLLOW']).send(self)
            return delete
        return False
