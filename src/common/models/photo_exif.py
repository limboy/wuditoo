#coding=utf-8
import logging
from collections import OrderedDict
import models

class Photo_Exif(models.base.BaseThing):
    def get(self, photo_id):
        self.reset()
        meta_dict = OrderedDict()
        meta = self.where('photo_id', '=', photo_id).order_by('id').findall()
        for item in meta:
            meta_dict[item.key] = item.value
        return meta_dict
