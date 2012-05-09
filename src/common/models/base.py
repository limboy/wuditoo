import logging

import thing
import json
from tornado.options import define, options
from macros.macro import REDIS_KEY
from utils import get_redis_client, attr_dict

thing.Thing.db_config(options.db_config)

class BaseThing(thing.Thing):
    def set_attr_by_req(self, arguments, *args):
        for item in args:
            setattr(self, item, arguments.get(item, [''])[0])

    def _after_insert(self):
        if self.table in ('user', 'photo'):
            redis_key = REDIS_KEY['TABLE_ITEMS'].format(table = self.table)
            redis_client = get_redis_client()
            redis_client.hset(redis_key, getattr(self, self._primary_key), json.dumps(self.to_dict()))

    def _after_update(self):
        self._after_insert()

    def _before_find(self, primary_key_value):
        if primary_key_value and self.table in ('user', 'photo'):
            redis_key = REDIS_KEY['TABLE_ITEMS'].format(table = self.table)
            redis_client = get_redis_client()
            result = redis_client.hget(redis_key, primary_key_value)
            return attr_dict(json.loads(result)) if result else None
