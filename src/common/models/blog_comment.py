#coding=utf-8

import models

class Blog_Comment(models.base.BaseThing):
    @property
    def creator(self):
        return models.user.User().find(self.user_id)
