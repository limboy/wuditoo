#coding=utf-8

from blinker import signal
import models
from macros.macro import EVENTS

blog_comment_add = signal(EVENTS['BLOG_COMMENT_ADD'])

class Blog(models.base.BaseThing):

    @property
    def creator(self):
        return models.user.User().find(self.user_id)

    @blog_comment_add.connect
    def _blog_comment_add(comment):
        blog = Blog().find(comment.blog_id)
        blog.comment_count += 1
        blog.save()
