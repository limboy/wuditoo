#!/usr/bin/env python
#coding=utf=8
import os
import sys

dirname = os.path.dirname
join = os.path.join

base_dir = os.path.abspath(dirname(dirname(__file__)))
nginx_dev_tpl = join(base_dir, 'etc', 'nginx', 'dev.conf.tpl')
nginx_dev_file = join(base_dir, 'etc', 'nginx', 'dev.conf')
redis_dev_tpl = join(base_dir, 'etc', 'redis', 'dev.conf.tpl')
redis_dev_file = join(base_dir, 'etc', 'redis', 'dev.conf')
supervisord_dev_tpl = join(base_dir, 'etc', 'supervisord', 'dev.conf.tpl')
supervisord_dev_file = join(base_dir, 'etc', 'supervisord', 'dev.conf')

for tpl, dev in {
        nginx_dev_tpl: nginx_dev_file, 
        redis_dev_tpl: redis_dev_file,
        supervisord_dev_tpl: supervisord_dev_file,
        }.items():
    with open(tpl, 'r') as f:
        cnt = f.read()
        cnt = cnt.replace('${base_dir}', base_dir+'/')
        with open(dev, 'w') as nf:
            nf.write(cnt)
        if tpl.find('nginx') != -1:
            print 'nginx conf generated at etc/nginx/dev.conf'
        elif tpl.find('redis') != -1:
            print 'redis conf generated at etc/redis/dev.conf'
        elif tpl.find('supervisord') != -1:
            print 'supervisord conf generated at etc/supervisord/dev.conf'
