---
title: Hexo 折腾记——自动部署篇
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 前端
	- blog
	- github
---



### 目标: 

写完一键上传并部署。(一个命令完成)

### 详细流程: 

上传图片至七牛，上传 deploy 文件至Github公开库 以及 博客源代码 至Github 私有库，Daocloud 检测到commit 自动构建镜像并自动更新应用。

<!--more-->


### 	实现:

1. 在public目录下放置Dockerfile文件:


``` docker
FROM daocloud.io/nginx
COPY ./ /usr/share/nginx/html
```

	
	
2. 在Daocloud里，创建新的代码构建，并设置成检测到commit就自动构建，再用这个镜像创建新应用，并设置自动更新

3. hexo根目录下创建 update.sh 

(Mac/Linux下需修改执行权限: sudo chown 755 ./update.sh， Windows 需改成对应的bat脚本)

``` bash
	#!/bin/sh
	# author: joway
	# 如果参数个数不等于0
	if test $# -gt 0
	then
	  if test $1 = '-img'
	  then
	    cd ./source/photos/
	    node photo-tool.js
	    cd ../../
	    echo 'Upload complete'
	  else
	    echo 'Parameter error'
	  fi
	else
	  echo 'No image needs upload'
	fi
	hexo clean
	hexo g && gulp
	hexo deploy
	git add .
	git commit -m 'update backup'
	git push origin master
```
	
命令使用:

``` bash
 # 需要上传图片
./update.sh -img  
#图片没改动， 只上传站点文件
./update.sh
```	


---


相关文章:


[Hexo折腾记——基本配置篇](https://joway.wang/posts/Hexo/2016-03-18-hexo-base.html)

[Hexo折腾记——性能优化篇](https://joway.wang/posts/Hexo/2016-03-19-Hexo-optimize.html)




