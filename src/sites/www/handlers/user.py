#coding=utf-8
import tornado
import models
import json
from base import (BaseHandler,
                  BasePhotosHandler,
                  BaseUserPhotosHandler,
                  BaseUsersHandler)
from utils import check_user_exists, process_avatar, hash_password
from helpers import get_avatar_url
from macros.macro import PHOTOS_PER_PAGE, MAX_AVATAR_SIZE, MAX_FOLLOW_NUM, MAX_UPLOAD_SIZE

class UserHandler(BaseUserPhotosHandler):
    @check_user_exists
    def get(self, username):
        return self._render('photos')

class UserPhotosHandler(BaseUserPhotosHandler):
    @check_user_exists
    def get(self, username):
        return self._render('photos')

class UserFollowingHandler(BaseUsersHandler):
    @check_user_exists
    def get(self, username):
        return self._render('following')

class UserFollowerHandler(BaseUsersHandler):
    @check_user_exists
    def get(self, username):
        return self._render('follower')

class MineFollowingHandler(BaseUsersHandler):
    @tornado.web.authenticated
    def get(self):
        return self._render('following', is_mine = True)

class MineFollowerHandler(BaseUsersHandler):
    @tornado.web.authenticated
    def get(self):
        return self._render('follower', is_mine = True)

class UserFollowHandler(BaseHandler):
    @check_user_exists
    @tornado.web.authenticated
    def post(self, username):
        if (not self.current_user.is_following(self.user.id) and 
            self.current_user.following_count < MAX_FOLLOW_NUM):
            models.FollowShip().follow(
                    self.current_user.id, self.user.id)
        else:
            models.FollowShip().unfollow(
                    self.current_user.id, self.user.id)
        return self.send_success_json()

class MinePhotosHandler(BasePhotosHandler):
    @tornado.web.authenticated
    def get(self):
        return self._render('mine_upload')

class MineLikesPhotosHandler(BasePhotosHandler):
    @tornado.web.authenticated
    def get(self):
        return self._render('mine_likes')

class MineInviteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        invite_keys = models.Invite_Key().findall_by_user_id(self.current_user.id)
        template_prefix = 'partial/' if self.is_ajax_request else 'mine_'
        return self.render('{0}invite_key.html'.format(template_prefix),
                            invite_keys = invite_keys)

class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        template = 'partial/settings.html' if self.is_ajax_request else 'settings.html'
        return self.render(template, 
                           profile = self.current_user.profile,
                           )

class SettingsProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        fullname = self.get_argument('fullname', '').strip()
        self.current_user.fullname = fullname
        self.current_user.save()
        if not self.current_user.saved:
            return self.send_error_json(self.current_user.errors)

        profile = self.current_user.profile
        profile.camera = self.get_argument('camera', '')
        profile.lens = self.get_argument('lens', '')
        profile.bio = self.get_argument('bio', '')
        profile.save()

        return self.send_success_json()

class SettingsLinkHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        profile = self.current_user.profile
        profile.link_weibo = self.get_argument('link_weibo', '')
        profile.link_qq = self.get_argument('link_qq', '')
        profile.link_douban = self.get_argument('link_douban', '')
        profile.link_flickr = self.get_argument('link_flickr', '')
        profile.link_blog = self.get_argument('link_blog', '')
        profile.save()

        if profile.saved:
            return self.send_success_json()
        return self.send_error_json(profile.errors)

class SettingsAvatarHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        def _send_result(status, content):
            data = {'status': status, 'content': content}
            return self.write("""
                    <script type = 'text/javascript'>
                    parent.avatarUploadDone({0})
                    </script>
                    """.format(json.dumps(data)))

        if not self.request.files:
            return _send_result('error', {'avatar': u'没有选择头像'})
        avatar_info = self.request.files['avatar'][0]
        if avatar_info['content_type'][:5] != 'image':
            return _send_result('error', {'avatar': u'这不是图片哦'})
        if len(avatar_info['body']) > (MAX_AVATAR_SIZE * 1024 * 1024):
            return _send_result('error', {'avatar': u'头像最大不能超过{0}M'.format(MAX_AVATAR_SIZE)})

        hash = process_avatar(avatar_info['body'], self.current_user.id)
        self.current_user.avatar_hash = hash
        self.current_user.save()
        avatar_url = get_avatar_url(self, self.current_user, 's')
        return _send_result('ok', {'avatar_url': avatar_url})

class SettingsPasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        changed = self.current_user.change_password(
                  self.get_argument('origin_password', ''),
                  self.get_argument('password', ''),
                  self.get_argument('password_confirm', ''))
        if changed:
            return self.send_success_json()
        return self.send_error_json(self.current_user.errors)

