#coding=utf-8
from tornado.options import define, options

define('db_master_url', default = 'mysql://root:123456@127.0.0.1:3306/wuditoo?charset=utf8', help = 'database master config')
define('db_slave_url', default = 'mysql://root:123456@127.0.0.1:3306/wuditoo?charset=utf8', help = 'database slave config')

db_config = {
    'master': {
        'url': options.db_master_url,
        'echo': False,
        },
    'slave': {
        'url': options.db_slave_url,
        'echo': False,
        },
}

define('db_config', default = db_config, help = 'database config')
