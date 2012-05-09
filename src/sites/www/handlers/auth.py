#coding=utf-8
import time
import logging
import tornado
from tornado.options import options
from base import BaseHandler
from utils import set_message, hash_password
import models

class RegisterHandler(BaseHandler):
    def get(self):
        invite_key = self.get_argument('invite_key', '')
        if not invite_key:
            return self.render('error/invite_key_missing.html')
        invite_key_info = models.Invite_Key().find_by_hash(invite_key)

        if not invite_key_info:
            return self.render('error/invite_key_invalid.html')
        if invite_key_info.used:
            return self.render('error/invite_key_used.html')
        return self.render('register.html', invite_key = invite_key)

    def post(self):
        user = models.User(
                username = self.get_argument('username', ''),
                email = self.get_argument('email', ''),
                password = self.get_argument('password', ''),
                password_confirm = self.get_argument('password_confirm', ''),
                invite_key = self.get_argument('invite_key', ''),
                )
        user_id = user.create()

        if not user_id:
            return self.send_error_json(user.errors)

        set_message(self, u'注册成功，有好的摄影作品别忘了来这里分享哦', 'info')
        self.set_secure_cookie('o_O', u'{0}'.format(user_id), domain='.{0}'.format(options.www_domain))
        return self.send_success_json(location = '/')

class LoginHandler(BaseHandler):
    def get(self):
        return self.render('login.html')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        if not username:
            return self.redirect(u'/login?error={0}'.format(u"用户名不能为空"))
        if not password:
            return self.redirect(u'/login?error={0}'.format(u"密码不能为空"))

        if username.find('@') != -1:
            user = models.User().find_by_email(username)
        else:
            user = models.User().find_by_username(username)

        if user:
            if user.password != hash_password(password):
                return self.redirect(u'/login?error={0}'.format(u"用户名与密码不符"))
        else:
            return self.redirect(u'/login?error={0}'.format(u"该用户不存在"))

        self.set_secure_cookie('o_O', u'{0}'.format(user.id), domain='.{0}'.format(options.www_domain))
        return_url = self.get_argument('return', '/')
        self.redirect(return_url)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('o_O', domain='.{0}'.format(options.www_domain))
        return self.redirect('/')
