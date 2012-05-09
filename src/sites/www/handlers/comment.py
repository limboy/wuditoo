#coding=utf-8
import logging
import time

from tornado.options import options
import tornado

from base import BaseHandler
import models

class CommentAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        photo_id = self.get_argument('photo_id', 0)
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.send_error_json({'message': 'photo not exists'})

        content = self.get_argument('content', '').strip()
        if not content:
            return self.send_error_json({'message': 'empty content'})

        comment = models.Photo_Comment(
                user_id = self.current_user.id,
                photo_id = photo.id,
                content = content,
                )
        comment.create()

        comment_content = self.render_string(
                'partial/comment.html',
                comment = comment,
                photo = photo,
                )

        return self.send_success_json(content = comment_content)

class CommentDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, comment_id):
        comment = models.Photo_Comment().find(comment_id)
        if comment and comment.status == 0:
            comment.delete()
            return self.send_success_json()
        return self.send_error_json({'message': 'error'})
