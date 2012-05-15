#coding=utf-8
import logging
import cProfile as profile
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
import config
tornado.options.parse_command_line()

import helpers
import routes

def create_app():
    settings = {
        'login_url': '/login',
        'static_path': 'src/sites/www/static',
        'template_path': 'src/sites/www/templates',
        'cookie_secret': '16oETzKXQAGaYdkL6gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
        'xsrf_cookies': False,
        'ui_methods': helpers,
        'debug': options.debug,
        #'autoescape': None,
    }
    return tornado.web.Application(routes.handlers, **settings)

def profile_patch():
    def wrapper(old_execute):
        def _(self, transforms, *args, **kwargs):
            if options.profile and self.get_argument('profile', 0):
                self.profiling = True
                self.profiler = profile.Profile()
                result = self.profiler.runcall(old_execute, self, transforms, *args, **kwargs)
                self.profiler.dump_stats(options.profile)
                return result
            else:
                self.profiling = False
                return old_execute(self, transforms, *args, **kwargs)
        return _

    old_execute = tornado.web.RequestHandler._execute
    tornado.web.RequestHandler._execute = wrapper(old_execute)

if __name__ == "__main__":
    profile_patch()
    app = create_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

