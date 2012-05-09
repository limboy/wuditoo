#coding=utf-8
from collections import OrderedDict

USERS_PER_PAGE = 20

PHOTOS_PER_PAGE = 15

MAX_PAGE = 15

MAX_FOLLOW_NUM = 450

BLOG_POSTS_PER_PAGE = 10

ACTIVITY_PER_PAGE = 20

PASSWORD_SALT = '!QAZ@WSXcde3)Okm9i'

MAX_UPLOAD_SIZE = 10

MAX_AVATAR_SIZE = 2

HOT_PHOTO_INTERVAL = 300

EVENTS = {
    'USER_ACTIVATION': 'user_activation',
    'USER_CREATE': 'user_create',
    'USER_FOLLOW': 'user_follow',
    'USER_UNFOLLOW': 'user_unfollow',
    'PHOTO_LIKE': 'photo_like',
    'PHOTO_UNLIKE': 'photo_unlike',
    'PHOTO_CREATE': 'photo_create',
    'PHOTO_UPLOAD': 'photo_upload',
    'PHOTO_DELETE': 'photo_delete',
    'PHOTO_COMMENT_ADD': 'photo_comment_add',
    'PHOTO_COMMENT_DELETE': 'photo_comment_delete',
    'BLOG_ADD': 'blog.after_insert',
    'BLOG_EDIT': 'blog.after_update',
    'BLOG_DELETE': 'blog_delete',
    'BLOG_COMMENT_ADD': 'blog_comment.after_insert',
}

ACTIVITY_ACTION = {
    'PHOTO_CREATE': 100,
    'PHOTO_LIKE': 101,
    'PHOTO_UNLIKE': 103,
    'PHOTO_COMMENT_ADD': 104,
    'PHOTO_COMMENT_DELETE': 105,
    'PHOTO_DELETE': 106,
    'USER_CREATE': 200,
    'USER_ACTIVATION': 201,
    'USER_FOLLOW': 202,
    'USER_UNFOLLOW': 203,
    'BLOG_ADD': 301,
    'BLOG_EDIT': 302,
    'BLOG_DELETE': 303,
    'BLOG_COMMENT_ADD': 304,
}

AVATAR_SIZE = {
    's': '48x48^',
    'm': '100x100^',
    'l': '160x160^',
}

PHOTO_SIZE = {
    's': '70x70^',
    'm': '215x215^',
    'l': '1200x12000',
}

REDIS_KEY = {
    'USER_PHOTO_COUNT': 'h_usr_pht_cnt',
    'USER_LIKED_COUNT': 'h_usr_lkd_cnt', # 被喜欢的次数
    'USER_LIKES_COUNT': 'h_usr_lks_cnt', # 喜欢的照片的张数
    'TABLE_ITEMS': 'h_tbl_tms:{table}',
    'USER_MESSAGE': 'l_usr_msg:{user_id}',
    'HOT_TAGS': 'set_hot_tags',
}

USER_LEVEL = [0, 10, 100, 500, 1000]
USER_LEVEL_CN = [u'小兔崽', u'功夫兔', u'普京兔', u'流氓兔', u'无敌兔']
USER_LEVEL_PHOTOS_PER_WEEK = [10, 20, 30, 40, 50]

INVITE_NUM = [5, 10, 15, 20, 25]
