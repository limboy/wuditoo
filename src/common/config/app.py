#coding=utf-8
from tornado.options import define, options

define('port', default = 9336, type = int, help = 'app listen port')
define('debug', default = True, type = bool, help = 'is debuging?')
define('profile', default = '/tmp/wuditoo.prof', type = str, help = 'profile')
define('photo_save_path', default = 'upload/photos', type = str, help = 'where to put user\'s photos')
define('avatar_save_path', default = 'upload/avatars', type = str, help = 'where to put avatars')
define('www_domain', default = 'lc.wuditoo.com', type = str, help = 'photo domain')
define('photo_domain', default = 'photo.lc.wuditoo.com', type = str, help = 'photo domain')
define('avatar_domain', default = 'avatar.lc.wuditoo.com', type = str, help = 'avatar domain')

options.log_file_prefix = 'log/wuditoo/web.log'
options.log_file_max_size = '50MB'
options.logging = 'debug' if options.debug else 'info'
