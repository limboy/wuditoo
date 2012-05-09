[unix_http_server]
file = var/svd.sock

[supervisorctl]
serverurl = unix://var/svd.sock

[supervisord]
logfile = log/supervisord/supervisord.log
logfile_maxbytes = 50MB
logfile_backups = 10
loglevel = info
pidfile = var/svd.pid

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[program:www]
command = python src/sites/www/app.py --port=9336 --debug=True --logging=debug --log_to_stderr=True --log_file_num_backups=1 --db_master_url=mysql://root:123456@127.0.0.1:3306/wuditoo?charset=utf8 --db_slave_url=mysql://root:123456@127.0.0.1:3306/wuditoo?charset=utf8
redirect_stderr = true
stdout_logfile = log/supervisord/www.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 1

[program:redis]
command = redis-server etc/redis/dev.conf
redirect_stderr = true
stdout_logfile = log/supervisord/redis.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 1
