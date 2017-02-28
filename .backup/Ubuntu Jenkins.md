# Ubuntu Jenkins

## Install
	
	wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
	sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
	sudo apt-get update
	sudo apt-get install jenkins
	
## Config

### 安装插件

第一次进入 jenkins 会让你修改密码，并安装推荐插件, 默认密码在服务器的文件中。

### 域名反向代理

默认开启在 8080 端口, 若要使用nginx反向代理, 需使用文档里推荐的conf来进行代理，否则部分功能会失常， 如下 , 把 server_name 换成自己的就行了:
	
	server {
	  listen          80;       # Listen on port 80 for IPv4 requests
	
	  server_name     jenkins.xxx.com;
	
	  #this is the jenkins web root directory (mentioned in the /etc/default/jenkins file)
	  root            /var/run/jenkins/war/;
	
	  access_log      /var/log/nginx/jenkins/access.log;
	  error_log       /var/log/nginx/jenkins/error.log;
	  ignore_invalid_headers off; #pass through headers from Jenkins which are considered invalid by Nginx server.
	  location ~ "^/static/[0-9a-fA-F]{8}\/(.*)$" {
	
	    #rewrite all static files into requests to the root
	    #E.g /static/12345678/css/something.css will become /css/something.css
	    rewrite "^/static/[0-9a-fA-F]{8}\/(.*)" /$1 last;
	  }
	
	  location /userContent {
	        #have nginx handle all the static requests to the userContent folder files
	        #note : This is the $JENKINS_HOME dir
		root /var/lib/jenkins/;
	        if (!-f $request_filename){
	           #this file does not exist, might be a directory or a /**view** url
	           rewrite (.*) /$1 last;
		   break;
	        }
		sendfile on;
	  }
	
	  location @jenkins {
	      sendfile off;
	      proxy_pass         http://127.0.0.1:8080;
	      proxy_redirect     default;
	
	      proxy_set_header   Host             $host;
	      proxy_set_header   X-Real-IP        $remote_addr;
	      proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
	      proxy_max_temp_file_size 0;
	
	      #this is the maximum upload size
	      client_max_body_size       10m;
	      client_body_buffer_size    128k;
	
	      proxy_connect_timeout      90;
	      proxy_send_timeout         90;
	      proxy_read_timeout         90;
	
	      proxy_buffer_size          4k;
	      proxy_buffers              4 32k;
	      proxy_busy_buffers_size    64k;
	      proxy_temp_file_write_size 64k;
	}
	
	  location / {
	
	     # Optional configuration to detect and redirect iPhones
	      if ($http_user_agent ~* '(iPhone|iPod)') {
	          rewrite ^/$ /view/iphone/ redirect;
	      }
	
	      try_files $uri @jenkins;
	   }
	}
	
	
### Git 私有仓库权限配置

1. 生成密钥:

		ssh-keygen -t rsa -C jenkins@xxx.com

2. 将密钥导入到 github 帐户中
3. 在jenkins 网页中, 添加 credentials , private key 如果设置成文件的话, 可能会出现权限错误, 我这边求简单直接选择 enter directly 填了文本信息


### 自动部署配置

1. 安装 Publish Over SSH 插件
2. 系统设置处 -> Publish over SSH 添加你的 Key ， 注意填写的是私钥 , 我直接在 Key 栏添加文本了
3. 接上 ， 添加 SSH Servers ，注意你的私钥对应的公钥必须写在你想要控制的服务器的 ~/.ssh/authorized_keys 文件里
4. 在项目配置里, 选择触发构建器 , GitHub hook trigger for GITScm polling 代表当 github push 了代码后, 则触发构建；Poll SCM 代表定期检测 Github 库代码变化
5. 在构建栏，配置 SSH Publishers	 , 这里的 Exec command 栏里的内容会在构建时执行
6. 构建后操作栏 同理