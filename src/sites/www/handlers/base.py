#coding=utf-8
import logging
from tornado.options import options
import tornado.web
import thing
import models
from macros.macro import PHOTOS_PER_PAGE, USERS_PER_PAGE
from utils import keep_order

class BaseHandler(tornado.web.RequestHandler):

    def send_error_json(self, data):
        return self.write({
            'status': 'error',
            'content': data
            })

    def send_success_json(self, **data):
        return self.write({
            'status': 'ok',
            'content': data
            })

    def get_current_user(self):
        user_id = self.get_secure_cookie('o_O')
        if not user_id:
            return None

        return models.User().find(user_id)

    @property
    def notification_count(self):
        return models.Notification().count_by_receiver_id_and_is_new(self.current_user.id, 1)

    @property
    def is_admin(self):
        return self.current_user and self.current_user.is_admin

    @property
    def is_ajax_request(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

class BasePhotosHandler(BaseHandler):
    def _render(self, kind, photo = None, tag_name = None):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        offset = (int(self.get_argument('page', 1)) - 1) * PHOTOS_PER_PAGE

        if kind == 'hot':
            page_path = '/photos/hot'
            photos_title = u'热门照片'
            photos_type = 'hot'
            photos = (models.Photo().order_by('-karma')
                      .findall_by_status(0, limit = PHOTOS_PER_PAGE, offset = offset))
            total_items = models.Photo().count_by_status(0)
        if kind == 'latest':
            page_path = '/photos/latest'
            photos_title = u'最新照片'
            photos_type = 'latest'
            photos = models.Photo().findall_by_status(0, limit = PHOTOS_PER_PAGE, offset = offset)
            total_items = models.Photo().count_by_status(0)
        elif kind == 'mine_upload':
            page_path = '/mine/photos'
            photos_title = u'我添加的照片'
            photos_type = 'user'
            photos = models.Photo().findall_by_user_id_and_status(
                self.current_user.id, 0, limit = PHOTOS_PER_PAGE, offset = offset)
            total_items = models.Photo().count_by_user_id_and_status(self.current_user.id, 0)
        elif kind == 'mine_likes':
            page_path = '/mine/likes_photos'
            photos_title = u'我喜欢的照片'
            photos_type = 'user'
            photo_ids = models.Photo_Like().findall_by_user_id(
                        self.current_user.id, limit = PHOTOS_PER_PAGE, offset = offset)\
                        .get_field('photo_id')
            photos = []
            for photo_id in photo_ids:
                photos.append(models.Photo().find(photo_id))

            total_items = models.Photo_Like().count_by_user_id(self.current_user.id)
        elif kind == 'tag':
            page_path = u'/tag/{0}'.format(tag_name)
            photos_title = u'带有"{0}"标签的照片'.format(tag_name)
            photos_type = u'tag/{0}'.format(tag_name)
            photo_ids = models.Photo_Tag().findall_by_tag(
                        tag_name, limit = PHOTOS_PER_PAGE, offset = offset)\
                        .get_field('photo_id')
            photos = []
            for photo_id in photo_ids:
                photos.append(models.Photo().find(photo_id))

            total_items = models.Photo_Tag().count_by_tag(tag_name)

        return self.render('{0}photos.html'.format(template_prefix),
                photos_title = photos_title,
                photos_type = photos_type,
                photos = photos,
                total_items = total_items,
                page_path = page_path,
                current_photo = photo,
                )

class BaseUserPhotosHandler(BaseHandler):
    def _render(self, kind, photo = None):
        template_prefix = 'partial/' if self.is_ajax_request else 'user_'
        offset = (int(self.get_argument('page', 1)) - 1) * PHOTOS_PER_PAGE

        fullname = self.user.fullname
        if self.current_user and self.user.id == self.current_user.id:
            fullname = u'我'

        if kind == 'photos':
            page_path = '/user/{0}/photos'.format(self.user.username)
            photos_title = u'{0}的照片'.format(fullname)
            photos_type = 'user'
            photos = models.Photo().findall_by_user_id_and_status(
                self.user.id, 0, limit = PHOTOS_PER_PAGE, offset = offset)
            total_items = models.Photo().count_by_user_id_and_status(self.user.id, 0)

        return self.render('{0}photos.html'.format(template_prefix),
                photos_title = photos_title,
                photos_type = photos_type,
                photos = photos,
                total_items = total_items,
                page_path = page_path,
                current_photo = photo,
                )

class BaseUsersHandler(BaseHandler):
    def _render(self, kind, is_mine = False):
        template_prefix = 'partial/' if self.is_ajax_request else (
                'mine_' if is_mine else 'user_')
        offset = (int(self.get_argument('page', 1)) - 1) * USERS_PER_PAGE

        user = self.user if not is_mine else self.current_user

        if kind == 'following':
            page_path = '/user/{0}/following'.format(user.username) if not is_mine else '/mine/following'
            users_title = u'{0}关注的人'.format(user.fullname if not is_mine else u'我')
            user_ids = models.FollowShip().findall_by_follower_user_id(
                user.id, limit = USERS_PER_PAGE, offset = offset).get_field('followed_user_id')
            users = []
            for user_id in user_ids:
                users.append(models.User().find(user_id))
            total_items = models.FollowShip().count_by_follower_user_id(user.id)

        if kind == 'follower':
            page_path = '/user/{0}/follower'.format(user.username) if not is_mine else '/mine/follower'
            users_title = u'关注{0}的人'.format(user.fullname if not is_mine else u'我')
            user_ids = models.FollowShip().findall_by_followed_user_id(
                user.id, limit = USERS_PER_PAGE, offset = offset).get_field('follower_user_id')
            users = []
            for user_id in user_ids:
                users.append(models.User().find(user_id))
            total_items = models.FollowShip().count_by_followed_user_id(user.id)

        return self.render('{0}users.html'.format(template_prefix),
                users_title = users_title,
                users = users,
                total_items = total_items,
                page_path = page_path,
                )

