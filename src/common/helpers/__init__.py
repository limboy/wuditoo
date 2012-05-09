#coding=utf-8
from urlparse import urlparse
import re
import markdown
import random
from datetime import datetime
import logging
from tornado.options import options
from macros.macro import REDIS_KEY
from utils import get_redis_client

def get_avatar_url(handler, user, size):
    if not user.avatar_hash:
        return '/static/img/default_avatar_{0}.jpg'.format(size)
    return 'http://{domain}/{user.id}/{user.avatar_hash}/{size}.jpg'.format(
            domain = options.avatar_domain,
            user = user,
            size = size)

def get_photo_url(handler, photo, size):
    return "http://{photo_domain}/{photo.user_id}/{photo.hash}/{size}.jpg".format(
            photo_domain = options.photo_domain,
            photo = photo,
            size = size)

def get_host(handler, url):
    host = urlparse(url).netloc
    host_sections = host.split('.')
    return '{0}.{1}'.format(host_sections[-2], host_sections[-1])

def get_message(handler):
    if handler.current_user:
        redis_client = get_redis_client()
        redis_key = REDIS_KEY['USER_MESSAGE'].format(user_id = handler.current_user.id)
        if redis_client.llen(redis_key):
            return redis_client.rpop(redis_key).split('|')

    message = handler.get_cookie('message')
    handler.clear_cookie('message')
    return message.split('|') if message else None

def timesince(handler, dt, default=u"just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    diff = datetime.now() - datetime.fromtimestamp(dt)
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

def render_comment(handler, content):
    result = re.sub(r'@([^\(]+)\((.*?)\)', r'@<a href="/user/\2">\1</a>', content)
    return nl2br(handler, result)

def md2html(handler, content):
    return markdown.markdown(content)

def nl2br(handler, content):
    return content.replace("\n", '<br />')

def home_sentence(handler):
    sentences = [
            u'开始不过迷上了相机这个尤物，结果却爱上了摄影这门艺术。',
            u'在我看来，某个东西你不把它拍下来就不能说你见过。-- Emile Zola',
            u'一张技术上完美的照片可能是世上最乏味的图像。 -- Andreas Feininger',
            u'我最好的作品常常是无意识的，且超出我理解能力之外的。 -- Sam Abell',
            u'不在于对相机的投入，而在于对相机的透入。 -- David L. Rayfield',
            u'你必须对运气做好准备。 -- Neil Leifer',
            u'相机如果不是诗人脑袋上的一只眼睛，其中的胶卷就没用。 -- Orson Welles',
            u'有时最简单的照片是最难拍的。 -- Neil Leifer',
            u'我真的相信有些东西如果我不拍下来就没人会看见。 -- Diane Arbus',
            u'别跟我说你没拍着的照片，就让我看看你拍到的好照片。 -- Edward K. Thompson',
            u'拍一个蛋糕也能成为艺术品。 -- Irving Penn',
            u'好照片是技术和艺术的成功合成。 -- Andreas Feininger',
            u'业余玩家的问题在于没有理由一定要拍照片。 -- Terence Donovan',
            u'只有好照片，没有好照片的准则。 -- Ansel Adams',
            u'找到最适合拍的是最难的。  -- Mary Ellen Mark',
            u'如果我知道如何拍出好照片，我每次都会拍出好照片了。 -- Robert Doisneau',
            u'有光即可摄影。 -- Alfred Stieglitz',
            u'摄影技艺的获得是靠花功而不是靠花钱。 -- Percy W. Harris',
            u'对于伟大的摄影作品，重要的是情深，而不是景深。 -- Peter Adams',
            u'最失落的两个职业是牙医和摄影师：牙医想当医生，摄影师想成为画家。 -- Pablo Picasso',
            u'光给了我创意的形状和脚本，也是我成为摄影师的原因。 -- Barbara Morgan',
            u'摄影是我的第二语言。 -- Gary Kapluggin',
            u'想象力跑焦了，眼力就靠不住了。 -- Mark Twain',
            u'摄影师必须是照片的一部分。 -- Arnold Newman',
            u'任一年中有12张有意义的照片就是一个好收获了。 -- Ansel Adams',
            u'除非景物使我感兴趣，否则我会略过不拍而节省我的胶卷以便拍更好的东西。 -- Andreas Feininger',
            u'一个真正的摄影师像真正的诗人或真正的画家那样少见。 -- Jean Cocteau',
            u'我们带到摄影中去的是所有我们读过的书，看过的电影，听过的音乐，爱过的人。 -- Ansel Adams',
            ]
    random.shuffle(sentences)
    return sentences[0]

def can_delete_photo(handler, photo):
    if handler.current_user and handler.current_user.id == photo.user_id:
        if not photo.likes_count and not photo.comments_count:
            return True
    return False
