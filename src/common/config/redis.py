#coding=utf-8
from tornado.options import define, options

define('redis_host', default = '127.0.0.1', help = 'master redis\'s host')
define('redis_port', default = 1860, type = int, help = 'master redis\'s port')
define('redis_db', default = 0, type = int, help = 'master redis\'s db')
define('redis_password', default = 'yes', help = 'master redis\'s password')
