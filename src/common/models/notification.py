#coding=utf-8
import time
import logging
import re
from blinker import signal

from macros.macro import EVENTS, ACTIVITY_ACTION
import models

photo_like = signal(EVENTS['PHOTO_LIKE'])
photo_comment_add = signal(EVENTS['PHOTO_COMMENT_ADD'])
blog_comment_add = signal(EVENTS['BLOG_COMMENT_ADD'])
user_follow = signal(EVENTS['USER_FOLLOW'])

class Notification(models.base.BaseThing):

    def save(self):
        #TODO add notification support
        return False

    @property
    def text(self):
        user = models.User().find(self.operator_id)
        text = ''
        if self.action == ACTIVITY_ACTION['PHOTO_LIKE']:
            photo = models.Photo().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 喜欢照片 <a href="/photo/{photo_id}">{photo_title}</a>'.format(
                    user = user,
                    photo_id = photo.id,
                    photo_title = photo.title or u"无标题",
                    )
        elif self.action == ACTIVITY_ACTION['PHOTO_COMMENT_ADD']:
            photo = models.Photo().find(self.context_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 评论了照片 <a href="/photo/{photo_id}">{photo_title}</a>'.format(
                    user = user,
                    photo_id = photo.id,
                    photo_title = photo.title or u"无标题",
                    )
        elif self.action == ACTIVITY_ACTION['BLOG_COMMENT_ADD']:
            post = models.Blog().find(self.context_id)
            title = u'评论了你在博文'
            url = '/blog/post/{post.id}'
            if post.status == 1:
                title = u'评论了你在反馈'
                url = '/feedback'
            text = u'<a href="/user/{user.username}">{user.fullname}</a> {title} <a href="{url}">{post.title}</a> 中的评论'.format(
                    user = user,
                    title = title,
                    post = post,
                    url = url,
                    )
        elif self.action == ACTIVITY_ACTION['USER_FOLLOW']:
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 关注了你'.format(user = user)

        return text

    @photo_like.connect
    def _photo_like(photo_like):
        receiver_id = models.Photo().find(photo_like.photo_id).user_id
        current_notification = Notification().where('receiver_id', '=', receiver_id)\
                               .where('operator_id', '=', photo_like.user_id)\
                               .where('action', '=', ACTIVITY_ACTION['PHOTO_LIKE'])\
                               .find()
        if not current_notification:
            Notification(
                operator_id = photo_like.user_id,
                receiver_id = receiver_id,
                action = ACTIVITY_ACTION['PHOTO_LIKE'],
                created = time.time(),
                target_id = photo_like.photo_id,
                is_new = 1,
                ).save()
        else:
            current_notification.is_new = 1
            current_notification.created = time.time()
            current_notification.save()

    @photo_comment_add.connect
    def _photo_comment_add(photo_comment):
        receiver_ids = set([models.Photo().find(photo_comment.photo_id).user_id])
        mention_users = re.findall(r'@[^\(]+\((.*?)\)', photo_comment.content)
        if mention_users:
            for username in mention_users:
                user_id = models.User().find_by_username(username).id
            receiver_ids.add(user_id)
        for receiver_id in receiver_ids:
            if photo_comment.user_id != receiver_id:
                Notification(
                    operator_id = photo_comment.user_id,
                    receiver_id = receiver_id,
                    action = ACTIVITY_ACTION['PHOTO_COMMENT_ADD'],
                    created = photo_comment.created,
                    target_id = photo_comment.id,
                    context_id = photo_comment.photo_id,
                    is_new = 1,
                    ).save()

    @user_follow.connect
    def _user_follow(user):
        current_notification = Notification().where('receiver_id', '=', user.followed_user_id)\
                               .where('operator_id', '=', user.follower_user_id)\
                               .where('action', '=', ACTIVITY_ACTION['USER_FOLLOW'])\
                               .find()
        if not current_notification:
            Notification(
                operator_id = user.follower_user_id,
                receiver_id = user.followed_user_id,
                action = ACTIVITY_ACTION['USER_FOLLOW'],
                created = time.time(),
                is_new = 1,
                ).save()
        else:
            current_notification.is_new = 1
            current_notification.created = time.time()
            current_notification.save()

    @blog_comment_add.connect
    def _blog_comment_add(blog_comment):
        receiver_ids = set([models.Blog().find(blog_comment.blog_id).user_id])
        mention_users = re.findall(r'@[^\(]+\((.*?)\)', blog_comment.content)
        if mention_users:
            for username in mention_users:
                user_id = models.User().find_by_username(username).id
            receiver_ids.add(user_id)
        for receiver_id in receiver_ids:
            if blog_comment.user_id != receiver_id:
                Notification(
                    operator_id = blog_comment.user_id,
                    receiver_id = receiver_id,
                    action = ACTIVITY_ACTION['BLOG_COMMENT_ADD'],
                    created = blog_comment.created,
                    target_id = blog_comment.id,
                    context_id = blog_comment.blog_id,
                    is_new = 1,
                    ).save()
