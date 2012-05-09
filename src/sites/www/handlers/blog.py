#coding=utf-8
import tornado
import models
import time
from handlers.base import BaseHandler

class BlogHandler(BaseHandler):
    def get(self, blog_id = 0):
        if not blog_id:
            blog = models.Blog().findall(limit=1).to_list()
            if blog:
                blog = blog[0]
        else:
            blog = models.Blog().find(blog_id)

        blog_comments = None
        if blog:
            blog_comments = models.Blog_Comment().findall_by_blog_id(blog.id)

        blogs = models.Blog().select(['id', 'title']).findall(limit=100)
        return self.render('blog/blog.html', 
                blog = blog,
                blogs = blogs,
                blog_comments = blog_comments,
                )

    @tornado.web.authenticated
    def post(self):
        if not self.current_user.is_admin:
            raise tornado.web.HTTPError(403)

        blog = models.Blog()
        if self.get_argument('id', ''):
            blog.id = self.get_argument('id')
        blog.title = self.get_argument('title')
        blog.content = self.get_argument('content')
        blog.created = blog.updated = time.time()
        blog.user_id = self.current_user.id
        blog.save()
        return self.redirect('/blog/{0}'.format(blog.id))

class BlogCommentAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, blog_id):
        if self.get_argument('content', ''):
            models.Blog_Comment(
                user_id = self.current_user.id,
                blog_id = blog_id,
                content = self.get_argument('content'),
                created = time.time(),
                updated = time.time(),
            ).save()
        return self.redirect('/blog/{0}'.format(blog_id))
