#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseHandler, BasePhotosHandler, BaseUserPhotosHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, PHOTOS_PER_PAGE
from helpers import nl2br
from utils import get_photo_exif, get_photo_width_height, check_photo_permission

class PhotoHandler(BaseHandler):
    def _incr_view_counts(self, photo):
        viewed_photo_ids = self.get_cookie('viewed_photo_ids', '').split(',')
        if str(photo.id) not in (viewed_photo_ids):
            viewed_photo_ids += [photo.id]
            photo.views_count += 1
            photo.save()
            self.set_cookie('viewed_photo_ids', ','.join(map(str, viewed_photo_ids)))

    def get(self, photo_id):
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.render('error/photo_not_exists.html')

        self._incr_view_counts(photo)
        
        return self.render('partial/photo.html',
                           photo = photo,
                           photo_exif = models.Photo_Exif().get(photo_id),
                           photo_tags = models.Photo_Tag().findall_by_photo_id(photo_id),
                           )

    @tornado.web.authenticated
    def post(self):
        photo = models.Photo(
                title = self.get_argument('title', ''),
                content = self.get_argument('content', ''),
                user_id = self.current_user.id,
                page_source = self.get_argument('page_source', ''),
                photo_source = self.get_argument('photo_source', ''),
                )
        photo_id = photo.create()

        if photo_id:
            photo.width, photo.height = get_photo_width_height(self.current_user.id, photo.hash)
            photo.save()

            tags = self.get_argument('tag', '')
            if tags:
                for tag in tags.split(' '):
                    models.Photo_Tag(photo_id = photo_id, tag = tag).save()
            
            if self.get_argument('exif_Model', ''):
                for item in ('Model', 'FocalLength', 'FNumber', 'ExposureTime', 'ISOSpeedRatings', 'Lens'):
                    value = self.get_argument('exif_{0}'.format(item), '')
                    models.Photo_Exif(
                            photo_id = photo_id,
                            key = item,
                            value = value).save()
            else:
                exif = get_photo_exif(photo.hash, self.current_user.id)
                for key, value in exif.items():
                    models.Photo_Exif(
                            photo_id = photo_id,
                            key = key,
                            value = value).save()

            self.send_success_json(location='/photo/{0}/via/mine'.format(photo_id))
        else:
            self.send_error_json(photo.errors)


class PhotoUpdateHandler(BaseHandler):
    @check_photo_permission
    @tornado.web.authenticated
    def post(self, photo_id):
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        if title:
            self.photo.title = title
            self.photo.content = content
            self.photo.save()
            return self.send_success_json()
        return self.send_error_json({'message': 'update failed'})

class PhotoLikeHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, photo_id):
        photo = models.Photo().find(photo_id)
        if not photo:
            return self.render('error/photo_not_exists.html')

        if not self.current_user.has_liked_photo(photo):
            models.Photo_Like().like(self.current_user.id, photo_id)
        else:
            models.Photo_Like().unlike(self.current_user.id, photo_id)
        return self.send_success_json()

class PhotoUploadHandler(BaseHandler):
    def get(self):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        return self.render('{0}upload.html'.format(template_prefix))

class HotPhotosHandler(BasePhotosHandler):
    def get(self):
        return self._render('hot')

class LatestPhotosHandler(BasePhotosHandler):
    def get(self):
        return self._render('latest')

class PhotoUserHandler(BaseUserPhotosHandler):
    def get(self, photo_id):
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.render('error/photo_not_exists.html')

        # used in BaseUserPhotosHandler
        self.user = models.User().find(photo.user_id)
        return self._render('photos', photo = photo)

class PhotoMineHandler(BasePhotosHandler):
    def get(self, photo_id):
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.render('error/photo_not_exists.html')
        kind = 'mine_upload' if self.current_user else 'hot'
        return self._render(kind, photo = photo)

class PhotoHotHandler(BasePhotosHandler):
    def get(self, photo_id):
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.render('error/photo_not_exists.html')

        return self._render('hot', photo = photo)

class PhotoTagHandler(BasePhotosHandler):
    def get(self, photo_id, tag_name):
        photo = models.Photo().find(photo_id)
        if not photo or photo.status != 0:
            return self.render('error/photo_not_exists.html')

        return self._render('tag', photo = photo, tag_name = tag_name)

class PhotosTagHandler(BasePhotosHandler):
    def get(self, tag_name):
        return self._render('tag', tag_name = tag_name)

class PhotoTagAddHandler(BaseHandler):
    @check_photo_permission
    @tornado.web.authenticated
    def post(self, photo_id):
        tags = self.get_argument('tag', '').split(' ')
        for tag in tags:
            if tag:
                models.Photo_Tag(
                        photo_id = self.photo.id,
                        tag = tag
                        ).save()

        return self.send_success_json(tags = tags)

class PhotoTagRemoveHandler(BaseHandler):
    @check_photo_permission
    @tornado.web.authenticated
    def post(self, photo_id, tag_id):
        tag = models.Photo_Tag().find(tag_id)
        if tag and tag.photo_id == self.photo.id:
            tag.delete()
            return self.send_success_json()
        return self.send_error_json({'message': 'invalid tag id'})

class PhotoDeleteHandler(BaseHandler):
    @check_photo_permission
    @tornado.web.authenticated
    def post(self, photo_id):
        self.photo.delete()
        return self.send_success_json(location = '/')
