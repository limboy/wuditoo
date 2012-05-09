#coding=utf-8
import time
import logging
from blinker import signal

from helpers import get_photo_url
from macros.macro import EVENTS, ACTIVITY_ACTION
import models

photo_create = signal(EVENTS['PHOTO_CREATE'])
photo_like = signal(EVENTS['PHOTO_LIKE'])
photo_upload = signal(EVENTS['PHOTO_UPLOAD'])
photo_unlike = signal(EVENTS['PHOTO_UNLIKE'])
photo_comment_add = signal(EVENTS['PHOTO_COMMENT_ADD'])
photo_comment_delete = signal(EVENTS['PHOTO_COMMENT_DELETE'])
user_create = signal(EVENTS['USER_CREATE'])
user_follow = signal(EVENTS['USER_FOLLOW'])
user_unfollow = signal(EVENTS['USER_UNFOLLOW'])
blog_add = signal(EVENTS['BLOG_ADD'])
blog_edit = signal(EVENTS['BLOG_EDIT'])
blog_comment_add = signal(EVENTS['BLOG_COMMENT_ADD'])

class Activity(models.base.BaseThing):
    @property
    def text(self):
        user = models.User().find(self.user_id)
        text = ''
        if self.action == ACTIVITY_ACTION['PHOTO_LIKE']:
            photo = models.Photo().find(self.target_id)
            photo_url = get_photo_url(self, photo, 's')
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 喜欢照片 <a href="/photo/{photo_id}"><img src="{photo_url}" /></a>'.format(
                    user = user,
                    photo_id = photo.id,
                    photo_url = photo_url,
                    )
        if self.action == ACTIVITY_ACTION['PHOTO_UNLIKE']:
            photo = models.Photo().find(self.target_id)
            photo_url = get_photo_url(self, photo, 's')
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 不喜欢照片 <a href="/photo/{photo_id}"><img src="{photo_url}" /></a>'.format(
                    user = user,
                    photo_id = photo.id,
                    photo_url = photo_url,
                    )
        elif self.action == ACTIVITY_ACTION['PHOTO_COMMENT_ADD']:
            photo = models.Photo().find(self.context_id)
            photo_url = get_photo_url(self, photo, 's')
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 评论了照片 <a href="/photo/{photo_id}"><img src="{photo_url}" /></a>'.format(
                    user = user,
                    photo_id = photo.id,
                    photo_url = photo_url,
                    )
        elif self.action == ACTIVITY_ACTION['BLOG_COMMENT_ADD']:
            post = models.Blog().find(self.context_id)
            title = u'评论了博文'
            url = '/blog/post/{post.id}'
            if post.status == 1:
                title = u'评论了反馈'
                url = '/feedback'
            text = u'<a href="/user/{user.username}">{user.fullname}</a> {title} <a href="{url}">{post.title}</a> 中的评论'.format(
                    user = user,
                    title = title,
                    post = post,
                    url = url,
                    )
        elif self.action == ACTIVITY_ACTION['USER_FOLLOW']:
            dest_user = models.User().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 关注了 <a href="/user/{user.username}">{dest_user.fullname}</a>'.format(user = user, dest_user = dest_user)
        elif self.action == ACTIVITY_ACTION['USER_UNFOLLOW']:
            dest_user = models.User().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 取消关注了 <a href="/user/{user.username}">{dest_user.fullname}</a>'.format(user = user, dest_user = dest_user)
        elif self.action == ACTIVITY_ACTION['USER_CREATE']:
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 创建了账号'
        elif self.action == ACTIVITY_ACTION['PHOTO_CREATE']:
            photo = models.Photo().find(self.target_id)
            photo_url = get_photo_url(self, photo, 's')
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 发布了照片 <a href="/photo/{photo.id}"><img src="{photo_url}" /></a>'.format(user = user, photo = photo, photo_url = photo_url)
        elif self.action == ACTIVITY_ACTION['BLOG_EDIT']:
            post = models.Blog().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 编辑了博文 <a href="/blog/post/{post.id}">{post.title}</a>'.format(user = user, post = post)
        elif self.action == ACTIVITY_ACTION['BLOG_ADD']:
            post = models.Blog().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 发布了博文 <a href="/blog/post/{post.id}">{post.title}</a>'.format(user = user, post = post)
        elif self.action == ACTIVITY_ACTION['BLOG_DELETE']:
            post = models.Blog().find(self.target_id)
            text = u'<a href="/user/{user.username}">{user.fullname}</a> 删除了博文 <a href="/blog/post/{post.id}">{post.title}</a>'.format(user = user, post = post)
        return text

    @property
    def feed_text(self):
        user = models.User().find(self.user_id)
        text = ''
        if self.action == ACTIVITY_ACTION['PHOTO_CREATE']:
            text = u'{user} 添加了这张照片'.format(user = user.fullname)
        elif self.action == ACTIVITY_ACTION['PHOTO_LIKE']:
            text = u'{user} 喜欢这张照片'.format(user = user.fullname)
        elif self.action == ACTIVITY_ACTION['PHOTO_COMMENT_ADD']:
            text = u'{user} 评论了这张照片'.format(user = user.fullname)
        return text

    def get_feed(self, user_ids, limit = 15, offset = 0):
        return self.where('user_id', 'in', user_ids)\
                   .where('action', 'in', [
                       ACTIVITY_ACTION['PHOTO_CREATE'],
                       ACTIVITY_ACTION['PHOTO_LIKE'],
                       ACTIVITY_ACTION['PHOTO_COMMENT_ADD'],
                       ])\
                   .findall(limit = limit, offset = offset)

    def get_feed_count(self, user_ids):
        return self.where('user_id', 'in', user_ids)\
                   .where('action', 'in', [ACTIVITY_ACTION['PHOTO_CREATE'], ACTIVITY_ACTION['PHOTO_LIKE']])\
                   .count()

    @photo_create.connect
    def _photo_create(photo):
        Activity(
            user_id = photo.user_id,
            action = ACTIVITY_ACTION['PHOTO_CREATE'],
            created = photo.created,
            target_id = photo.id,
            ).save()

    @photo_like.connect
    def _photo_like(photo_like):
        Activity(
            user_id = photo_like.user_id,
            action = ACTIVITY_ACTION['PHOTO_LIKE'],
            created = time.time(),
            target_id = photo_like.photo_id,
            ).save()

    @photo_unlike.connect
    def _photo_unlike(photo_like):
        Activity(
            user_id = photo_like.user_id,
            action = ACTIVITY_ACTION['PHOTO_UNLIKE'],
            created = time.time(),
            target_id = photo_like.photo_id,
            ).save()

    @photo_upload.connect
    def _photo_upload(photo):
        Activity(
            user_id = photo.user_id,
            action = ACTIVITY_ACTION['PHOTO_UPLOAD'],
            created = photo.created,
            target_id = photo.id,
            ).save()

    @user_create.connect
    def _user_create(user, **kwargs):
        Activity(
            user_id = user.id,
            action = ACTIVITY_ACTION['USER_CREATE'],
            created = user.created,
            ).save()

    @user_follow.connect
    def _user_follow(user):
        Activity(
            user_id = user.follower_user_id,
            action = ACTIVITY_ACTION['USER_FOLLOW'],
            target_id = user.followed_user_id,
            created = time.time(),
            ).save()

    @user_unfollow.connect
    def _user_unfollow(user):
        Activity(
            user_id = user.follower_user_id,
            action = ACTIVITY_ACTION['USER_UNFOLLOW'],
            target_id = user.followed_user_id,
            created = time.time(),
            ).save()

    @photo_comment_add.connect
    def _photo_comment_add(photo_comment):
        activity = Activity(
                user_id = photo_comment.user_id,
                action = ACTIVITY_ACTION['PHOTO_COMMENT_ADD'],
                target_id = photo_comment.id,
                created = photo_comment.created,
                context_id = photo_comment.photo_id,
                ).save()

    @blog_add.connect
    def _blog_add(blog):
        activity = Activity(
                user_id = blog.user_id,
                action = ACTIVITY_ACTION['BLOG_ADD'],
                target_id = blog.id,
                created = blog.created,
                ).save()

    @blog_edit.connect
    def _blog_edit(blog):
        action = ACTIVITY_ACTION['BLOG_EDIT'] if blog.status == 0 else ACTIVITY_ACTION['BLOG_DELETE']
        activity = Activity(
                user_id = blog.user_id,
                action = action,
                target_id = blog.id,
                created = time.time(),
                ).save()

    @blog_comment_add.connect
    def _blog_comment_add(comment):
        activity = Activity(
                user_id = comment.user_id,
                action = ACTIVITY_ACTION['BLOG_COMMENT_ADD'],
                target_id = comment.id,
                created = comment.created,
                context_id = comment.blog_id,
                ).save()
