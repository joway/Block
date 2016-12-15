---
title: Web服务器原理 以及 Django && uWSGI && Nginx 部署
comments: true
categories: django
toc: true
tags:
	- django
	- docker
	- nginx
	- uwsgi
---

### 前言

之前部署 Django 应用都是通过django自带的一个服务器来进行非常简单的部署 (直接执行 python manage.py runserver ) 。但是后来看一篇文章才知道 runserver 命令唤起的是开发服务器，并不能很好地应用于生产环境。而在生产环境下部署python代码的方式其实有很多种，这里我选择 uWSGI 的方式。

<!-- more -->

之前我一直不理解为什么要单独搞这么一套东西来进行部署，在以往的经验里，我以为一个web服务器无非就是把代码运行起来，占用一个端口而已。这里整理下最近的学习体会。

### Java Web Server

在java web 里 ，部署的确是非常之简单，打成一个war包，所有的依赖都封装起来了，之后丢进 tomcat 容器里就能非常简单地运行了。在这种架构里，tomcat 就是 web server , 流程如下:

> the web client 
> <-> 
> Server(顶层类元素：一个配置文件中只能有一个<Server>元素，可包含多个Service。) 
> <->
> Service(顶层类元素：本身不是容器，可包含一个Engine，多个Connector。) 
> <-> 
> Connector（连接器类元素：代表通信接口,连接请求至web application,支持HTTP和AJP协议）
> <-> 
> Engine( 容器类元素：为特定的Service组件处理所有客户请求，可包含多个Host。)
> <-> 
> Host（容器类元素：为特定的虚拟主机处理所有客户请求，可包含多个Context） 
> <-> 
> Context (容器类元素：为特定的Web应用处理所有客户请求)

简单来说:

- 获取连接 /index.html
- Connector 模块将请求(Request)传递给 Container 模块
- Container 分析HTPP请求信息，组装成 HttpServletRequest 对象
- 创建新的HttpServletResponse对象
- 根据路由配置，搜索相应的Servlet，并创建一个线程用于处理本次请求。此时线程会将上面Request和Response对象的索引，传递给Servlet
- 新线程中的 Servlet 调用其service方法，进行业务处理
- 线程结束后，通过HttpServletResponse对象的PrintWriter，返回浏览器一个信息
- 关闭连接

一个servlet实现类只会有一个实例对象，多个线程是可能会访问同一个servlet实例对象的， 所以servlet不是线程安全的，故而servlet的全局变量和静态变量必须小心。

注意，servlet 只是 java 自己的规范，而在Python中，它也有自己的一套规范 。

### Python Web Server

架构大致如下:

> the web client 
> <-> the web server(nginx) 
> <-> the socket 
> <-> uwsgi 
> <-> Django

其中 the socket <-> uwsgi <-> Django 可被 docker 包装进容器，nginx 作为分发器。

python 中的规范为 WSGI ， 它定义了：web应用（或者web框架）与 web服务器交互接口(WSGI)。而uWSGI就是一个支持WSGI规范的web服务器。把web应用部署到uWSGI中，当 uWSGI 接受到请求时，会按照WSGI定义的接口调用 web 应用处理。(在java里应用部署到Tomcat，然后Tomcat按照servlet规范回调web应用) 

事实上，任何Web服务器都可以看作如下的函数调用

```
	def simple_app(environ, start_response):
				# 业务逻辑处理
	        status = '200 OK'
	        response_headers = [('Content-type','text/plain')]
	        start_response(status, response_headers)
	        return ['Hello world!\n']
	
	    application = simple_app # 若web应用部署在uWSGI容器中，需要这行代码

```

上面这个函数是 Web服务器 调用 Web应用 的一个示例：

- environ 变量中含各种请求头信息(视协议而定)
- start_response 是一个web服务器传过去的回调接口用来接受HTTP响应码以及HTTP响应头

uWSGI会把接收到的请求按照指定协议解析，然后把解析的结果（譬如：HTTP各请求头数据）设置到environ变量中，接着按照WSGI规范回调web应用（uWSGI默认回调application函数，并且传递environ和start_response两个参数），最终web应用开始处理请求（各种数据库查询，各种函数调用...）并把结果返回给uWSGI。

### uWSGI 部署

uWSGI 支持多种协议， 所以在架构中，并不一定要加入nginx， 可以直接拿uWSGI来作 http 服务器:

```
    $ uwsgi --http 127.0.0.1:8000 \
            --wsgi-file simple_app.py \ 
            --master --processes 2 \
            --daemonize /var/log/uwsgi.log \
            --pidfile /var/log/uwsgi.pid
```

而之所以要采用 nginx + uwsgi 方式部署，是因为 nginx 能够更加高效处理静态资源，同时还可以进行负载均衡，所以要在uwsgi上面再套一层:

```
	# http 启动方式下
	location / { 
	    include uwsgi_params;                                                                                
	    uwsgi_pass 127.0.0.1:8000;
	}
```

注意， 这里我们假设我们的 uwsgi 以http 方式开了8000 端口，这个时候事实上，我们直接用8000 端口就是能够访问的，也就是说，即便我们不用 uwsgi_pass , 用 标准的反向代理 : proxy_pass 也是可以转发的。

但是因为http协议本身是一个文本协议，解析起来非常耗时，所以在转发之前先把转换成其他协议（通常是二进制协议，譬如这里的uwsgi)。nginx会先把请求按照按照uwsgi协议转换（http -> wsgi），然后再转发给其他服务器处理。

有一个值得注意的问题是，uwsgi 本身就是支持了http协议，甚至支持了https协议，而如果你本身就只是提供一个restful API 而已，那么事实上是不需要nginx去参与的，即便Nginx参与了也不会提升性能，相反还多加了一层，uwsgi 服务器本身的性能就是高效的。但是目前网上几乎所有教程都在讲如何把uwsgi和nginx给整合起来，这个其实是很多人没有明白nginx和uwsgi的作用。

当然，仅仅只是当你的应用很简单，也没什么静态资源的时候，可以丢掉nginx，直接上uwsgi。但是如果你想要更加灵活配置站点，或者想加入负载均衡，或者有静态文件要部署，那么这个时候 nginx 才该发挥作用了。在 [serverfault](http://serverfault.com/questions/590819/why-do-i-need-nginx-when-i-have-uwsgi) 上一个人就讲了这点，虽然他只有一个wordpress 博客， 但是通过nginx ，他缓存文章内容24小时，缓存首页5分钟，这样即便是在动态网站下，也能高效地提升服务器并发能力。

另外一个问题是，uwsgi 在整合 nginx 的时候，支持以TCP port 和 Unix socket 两种协议，例如:

```
# TCP port: 
upstream django {
    server 127.0.0.1:8001; # for a web port socket
}

# Unix socket
upstream django {
    server unix:/chirp/chirp.sock; # for a file socket
}
```

使用 Unix socket 时，由于其文件在本机，故而其少了很多check 的步骤，相对来讲要快些，但是它是基于文件形式的，所以并发时候磁盘IO的影响也需要考虑，另外它由于是本地文件，也更加安全。Unix socket结合长链接配置，可以有效提高端口的复用率，明显提升服务器效率。但是长链接在并发时候也会影响到效率。

关于在实际应用中如何选择，我喜欢 stackoverflow 上的一个回答，对于这些底层协议选择之间的区别，虽然有，但是微乎其微。即便你底层优化再好————事实上现在的商用底层服务已经优化得很好了————你应用代码稍微乱写就能够把这些细微的效率提升给折腾没了。


### 参考资料:

[Nginx + uWSGI + Webpy配置&原理](https://github.com/diaocow/nginx_study/blob/master/Nginx%20%2B%20uWSGI%20%2B%20Webpy%E9%85%8D%E7%BD%AE%26%E5%8E%9F%E7%90%86.md)
[基于nginx和uWSGI在Ubuntu上部署Django](http://www.jianshu.com/p/e6ff4a28ab5a)
