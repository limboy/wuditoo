#coding=utf-8
import logging
import time

from tornado.options import options
import tornado.web

from common.macros.macro import PHOTOS_PER_PAGE
from base import BaseHandler, BasePhotosHandler
import models

class HomeHandler(BasePhotosHandler):
    def get(self):
        return self._render('hot')

class AboutHandler(BaseHandler):
    def get(self):
        return self.render('about.html')
