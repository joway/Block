# Block

> Another blog based on Django . 

## Usage

### Env

- Python 3.5.1
- Mysql
- Redis
- [Nginx]

### Install

	git clone 
	
	cd Block 
	
	pip install -r requirements.txt 
	
	python manage.py runserver 0.0.0.0:8000
	
### Custom

	cp prov_settings.py local_settings.py
	
	change env in local_settings.py
	
	
### Docker

	docker build . 
	
## Overview

### Article List

- 支持 tag 过滤
- 支持catagory 过滤

![](https://static.joway.wang/upload/14841134357.png)

### Article Detail

- markdown 支持
- mem cache

![](https://static.joway.wang/upload/14841135176.png)

### Comment

- 收到评论后邮件通知 ( 邮件服务使用 Amazon SES )
- 支持表情输入，支持 emoji

![](https://static.joway.wang/upload/14841135852.png)

![](https://static.joway.wang/upload/14841136332.png)

![](https://static.joway.wang/upload/14841207254.png)

### Create Article

- 支持 自动生成 tag

![](https://static.joway.wang/upload/14841193257.png)

### Profile

![](https://static.joway.wang/upload/14841151685.png)

### ImageBox

- 支持粘帖截图自动上传
- 支持预览图片
- 支持一键复制地址

![](https://static.joway.wang/upload/14841191114.png)

### Feeds

- celery + redis 实现分布式任务派发
- 自动更新 RSS 订阅

![](https://static.joway.wang/upload/14841176533.png)

### Analysis

![](https://static.joway.wang/upload/14841194008.png)

### Timeline

- 网站用户动态追踪

![](https://static.joway.wang/upload/14841194675.png)

### Search

- 使用 whoosh 进行全文搜索

![](https://static.joway.wang/upload/14841195369.png)

