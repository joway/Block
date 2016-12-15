---
title: Hexo折腾记——统计与交互篇
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 前端
	- blog
	- github
---


### 前言

前面说到，由于天朝的网络原因， 导致 Google Analytics 和 Disqus 的js加载特别慢，但是又不能去掉最最基本的统计与用户交互功能，国内的百度统计和多说都做的很垃圾，多说其实还不错，就是评论者头像是加载原登陆站点的，不支持https，还老是发抽。偶然看到大神的 [CodeVS](http://codevs.cn) 用了Growing 来作统计分析，用了DaoVoice来进行用户反馈，觉得比谷歌分析友好多了，于是便拿来耍了几下。

<!--more-->


### 配置Growing

网址 : [Growing.io](https://growing.io)

进去注册以后，它会让你选择平台(网站/安卓/ios)，选择网站(如果选择app，则要在app内编码)，分配给你一个js脚本，把它放在网页中就行了。

我是放在模板文件的footer.ejs中。这样每个页面都会加载。

growing 的优势在于，它不仅仅能统计用户的访问，还能统计用户什么时间点击了什么链结。

![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-25%2019.52.18.png?imageView2/2/w/500)

### 配置 DaoVoice

网址: [DaoVoice](http://dashboard.daovoice.io/#/get-started)

进入并登陆后，有如下页面:

![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-25%2019.45.12.png?imageView2/2/w/500)

选择访客接入(除非你有自己的用户模块)

待你把上面的js脚本放到网站上并生效后，会自动跳到下一步，然后就能在页面显示我博客右下角的小图标啦。~

可以在后台配置图标样式，以及回复用户反馈~


PS: DaoVoice并不能替代评论功能，但是可以作为一个不错的交(gao)友(ji)平台(虽然它本来是用来反馈意见的233333)


### 配置 OneApm

网址: [oneapm](http://www.oneapm.com/)


一个很好的分析应用和服务器性能详尽情况的工具，安装简单，即插即用

![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-29%2018.05.31.png)


![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-29%2018.05.57.png)

![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-29%2018.06.15.png)

![](https://dn-joway.qbox.me/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-03-29%2018.06.33.png)
