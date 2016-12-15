---
title: OpenResty OS X 配置小记
comments: true
categories: docker
toc: true
tags:
	- openresty
	- nginx
	- osx
---


### 前言

基本的安装过程在官网上已经有了示例，不过由于 OpenResty 本身就不是一个面向新手的东西，许多地方都没有具体说明步骤以及有可能遇到的坑。再加上这个东西又是编译安装的，所以不同平台，不同环境下可能会遭受了各类问题。这里记录下我学习和配置的过程 。

<!--more-->

### 为什么要用OpenResty

OpenResty 在企业级应用里有各种各样的用法，这里只是讲下我个人的需求。

Nginx 本身是一个性能卓越但是偏向于静态资源的应用服务器，我拿它来做得最多的事情就是「静态文件部署」,「反向代理」和「负载均衡」了，我个人的常见使用过程例如: 用docker打包一个应用进容器(django -> uwsgi -> nginx)，利用 nginx 开放出一个端口(例如32101)，然后再在宿主服务器的 nginx 里作**反向代理**, 把域名转发到这个端口上，也可以用**负载均衡**分发到不同的服务器或容器里。这种做法的好处是不管是动态静态的资源，全部可以封装成一个容器，宿主只是作一个转发作用而已。

但是单纯的nginx应用的弊端是，我要到最后的应用里才能取得真正的请求，如果我想在一开始就对请求进行一些操作甚至是业务逻辑就显得极为麻烦。OpenRestry 就是一个nginx上的拓展，便于在nginx上直接开发功能，高效地处理请求。甚至可以承担部分业务逻辑的功能。理论上讲，甚至可以直接用户lua在nginx上直接开发高性能应用。


### OS X 下安装 OpenRestry

- 相关库安装:
	
```
	brew update
	brew install pcre openssl
```
	
	openssl 安装完成后，记住其安装目录。之后编译的时候需要得到它的源码地址
	
- 编译并安装 openrestry :

```
	# 下载源码
	wget https://openresty.org/download/openresty-1.9.15.1.tar.gz
	tar xzvf ngx_openresty-1.9.15.1.tar.gz
	
	# 进入目录
	cd ngx_openresty-1.9.15.1
	
	./configure --prefix=/opt/openresty\
             --with-cc-opt="-I/usr/local/include"\
             --with-luajit\
             --without-http_redis2_module \
             --with-ld-opt="-L/usr/local/lib"
             
   # 这一步的时候，如果报错了, 就在最后加上:
   
   --with-openssl=/usr/local/Cellar/openssl/1.0.2h
   #这个目录根据你的openssl 版本而定，注意，这里的是源码目录，不是openssl安装目录!
  	如果设置了openssl 目录仍旧无效，可尝试:
  	
	brew uninstall openssl --force
	brew install openssl
   
    # 然后开始make and install, 可能需要sudo权限:
   
    make
    make install
    
```

### Nginx 配置:

官网文档里说把nginx的配置目录从安装目录和工作目录分开的一个办法就是: 

```
	mkdir ~/openresty-test ~/openresty-test/logs/ ~/openresty-test/conf/
	# add my_nginx.conf
	...
	
	nginx -p ~/openresty-test
```

之后nginx就按这个文件夹里的配置来操作，日志也进入这边。

但是这边有一个小问题就是,如果设定了 -p 参数，相当于把nginx的默目录从默认的/opt/openresty/nginx/ 转到了 ~/openresty-test 下，注意，这种转移只对这条命令本身是有效的，再一次运行nginx的时候，仍旧会回到原本的目录下。所以使用这种方式的时候，要注意之后的reload 等命令下的nginx都要加上这个-p的参数。

文档里的思想是每个项目都配置自己独立的conf和log目录，启动一个独立的nginx进程，但是在本地测试环境的时候，可能并不需要这么高的独立性，我为了方便，设置了一个**主工作目录**, 在这个目录里可以配置多个conf文件，便于学习和测试时的使用。


首先 ，我们按照上面的步骤建立一个openresty目录:
	
	/Users/joway/openresty
	├── conf
	└── logs

可以通过修改目录下的 nginx.conf, 把在 conf.d 下的配置文件导入进nginx.conf来进行多conf管理 ，在自带的nginx.conf 加上一句:

```
	http {
		...
		
		include conf.d/*.conf;
	}

```

然后在conf目录下新建一个conf.d目录， 之后把我的自定义的配置文件都加在这里，以 .conf 结尾

之后就能够使用 sudo nginx -p ~/openresty -s reload 来调用了，为了方便我设置了一个alias:

	alias resty='sudo nginx -p ~/OpenResty
	
之后要添加新的conf，就在conf/conf.d/目录下放入新的xxx.conf 文件。

如果要单独对某个conf文件生效，可使用:

	resty -c path/xxx.conf
	
	
