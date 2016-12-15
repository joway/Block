---
title: Django && uWSGI && Nginx 在Docker中的部署
comments: true
categories: docker
toc: true
tags:
	- django
	- docker
	- nginx
	- uwsgi
---

### 基础架构

上一篇讲了 Django && uWSGI && Nginx 的基本逻辑和部署，这里我把它移至进docker中。

我的应用架构是:

> 分发器(Nginx) -> docker 容器 (Nginx -> uWSGI -> Django)

<!-- more -->

分发器只作如下事情:

1. 域名配置(http/https)
2. localtion 匹配分发
3. 负载均衡

针对每个应用的详细配置由 docker 中的 Nginx 来进行(例如开启gzip ，缓存等)。

### Django <-> uWSGI

这里使用 supervisord 来进行部署，supervisord.conf 文件如下:

```
[program:uwsgi-app]
command = /usr/local/bin/uwsgi --ini /chirp/.deploy/uwsgi.ini

[program:nginx-app]
command = /usr/sbin/nginx
```

uwsgi.ini 文件如下:

```
[uwsgi]
ini = :base
socket=/chirp/chirp.sock
master=True
processes= 10

[base]
# chdir to the folder of this config file, plus app/website
chdir=/chirp
# load the module from wsgi.py, it is a python path from
# the directory above.
module=config.wsgi:application
# allow anyone to connect to the socket. This is very permissive
chmod-socket=666
```

这里说明下，socket=/chirp/chirp.sock 表示我使用了 unix socket 方式进行通信。chmod-socket=666 是为了使得socket 文件进行权限控制。

启动命令:

	CMD ["supervisord", "-n"]


### uWSGI  <-> Nginx

nginx.conf :

```
# the upstream component nginx needs to connect to
upstream django {
    server unix:/chirp/chirp.sock; # UNIX socket
    # server 127.0.0.1:8001; # TCP port
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80 default_server;
    # the domain name it will serve for
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    # location /media  {
    #    alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
    # }

    # location /static {
    #    alias /path/to/your/mysite/static; # your Django project's static files - amend as required
    # }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /chirp/.deploy/uwsgi_params; # the uwsgi_params file you installed
    }
}
```

说明下，nginx 默认是以后端守护进程开启的，而supervisord 只能够针对front end 程序使用，所以一开始这边导致nginx一直在重启。

解决方法:

	RUN echo "daemon off;" >> /etc/nginx/nginx.conf

注意! daemon off; 只能通过dockerfile 方式写入原生nginx.conf 中，我自己的conf文件只能够进入到它的http{} 块中，是无效的，它必须定义在根块里。

### 完成Dockerfile

```
FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    mysql-client \
    nginx \
    supervisor

RUN mkdir /chirp
WORKDIR /chirp

# for cache
# Configure Nginx and uwsgi
ADD ./requirements.txt /chirp/requirements.txt
RUN rm /etc/nginx/sites-enabled/default
ADD ./.deploy/nginx.conf /etc/nginx/sites-enabled/chirp.conf
ADD ./.deploy/supervisord.conf /etc/supervisor/conf.d/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ADD . /chirp

EXPOSE 80
CMD ["supervisord", "-n"]
```