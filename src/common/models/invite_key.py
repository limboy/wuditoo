#coding=utf-8
import logging
from blinker import signal
import models
from macros.macro import EVENTS, INVITE_NUM
from utils import gen_invite_key

user_create = signal(EVENTS['USER_CREATE'])

class Invite_Key(models.base.BaseThing):
    @user_create.connect
    def _user_create(user, **kwargs):
        invite_key = Invite_Key().find_by_hash(kwargs['invite_key_hash'])
        invite_key.dest_user_id = user.id
        invite_key.used = 1
        invite_key.save()

        for i in range(INVITE_NUM[0]):
            Invite_Key(
                    user_id = user.id,
                    hash = gen_invite_key(),
                    ).save()

    def gen_by_level(self, user, level_current, level_prev):
        delta_key_num = INVITE_NUM[level_current] - INVITE_NUM[level_prev]
        for i in range(delta_key_num):
            Invite_Key(
                    user_id = user.id,
                    hash = gen_invite_key(),
                    ).save()

    @property
    def consumer(self):
        return models.User().find(self.dest_user_id)
